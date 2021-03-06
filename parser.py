import re
import os
from .node import Node, NodeType


class Parser:
  """
  Parses a behavior tree.

  ? ... !   - Priority node
  > ... <   - Sequence node
  // ... \\ - Parallel node
  /n/ .. \\ - Parallel node
  # ...     - Comment
  :...      - File (subtree)
  ...       - Action
  """
  @staticmethod
  def parse(behavior_tree):
    nodes = []
    while behavior_tree!="":
      #print "\n\n\033[33mparsing:\033[00m\n", behavior_tree
      behavior_tree = behavior_tree.strip('\n\t ')
      # raw_input("")

      if behavior_tree.startswith("?"):
        node, behavior_tree = Parser.priority(behavior_tree)

      elif behavior_tree.startswith(">"):
        node, behavior_tree = Parser.sequence(behavior_tree)

      elif behavior_tree.startswith("/"):
        node, behavior_tree = Parser.parallel(behavior_tree)

      elif behavior_tree.startswith("#"): # comment
        node, behavior_tree = Parser.comment(behavior_tree)

      elif behavior_tree.startswith(":"):
        node, behavior_tree = Parser.file(behavior_tree)

      else: # action
        node, behavior_tree = Parser.action(behavior_tree)

      if node is not None:
        nodes.append(node)

    return nodes

  @staticmethod
  def file(behavior_tree):
    end = behavior_tree.find("\n")
    if end is -1:
      end = len(behavior_tree)
    filename = behavior_tree[1:end]
    if not os.path.exists(filename):
      raise IOError("Subtree with filename "+os.getcwd()+os.sep+filename+" was not found.")
    with open(filename, 'r') as f:
      node = Parser.parse(f.read())[0]
    return node, behavior_tree[end:]

  @staticmethod
  def action(behavior_tree):
    match = re.match(r"\A([a-zA-Z0-9-_]+)", behavior_tree)
    if match is None:
      raise SyntaxWarning("Action could not be found.\n\""+behavior_tree+"\"")
    action = match.group(0)
    node = Node(
      NodeType.ACTION_CONDITION,
      action=action
    )
    return node, behavior_tree[len(action):]

  @staticmethod
  def comment(behavior_tree):
    end = behavior_tree.find("\n")
    if end is -1:
      end = len(behavior_tree)
    #print "is comment {}".format(behavior_tree.splitlines()[0])
    return None, behavior_tree[end:]

  @staticmethod
  def sequence(behavior_tree):
    opencount = 1;
    end = None
    for i in xrange(1,len(behavior_tree)):
      if behavior_tree[i] is '>':
        opencount += 1
      elif behavior_tree[i] is '<':
        opencount -= 1
        if opencount is 0:
          end = i
          break

    if end is None:
      raise SyntaxWarning("End not found while parsing BT sequence node.\n"+behavior_tree)

    node = Node(
      NodeType.SEQUENCE,
      children=Parser.parse(behavior_tree[1:end])
    )
    return node, behavior_tree[end+1:]

  @staticmethod
  def priority(behavior_tree):
    opencount = 1;
    end = None
    for i in xrange(1,len(behavior_tree)):
      if behavior_tree[i] == '?':
        opencount += 1
      elif behavior_tree[i] == '!':
        opencount -= 1
        if opencount is 0:
          end = i
          break

    if end is None:
      raise SyntaxWarning("End not found while parsing BT priority node.\n"+behavior_tree)

    node = Node(
      NodeType.PRIORITY,
      children=Parser.parse(behavior_tree[1:end])
    )
    return node, behavior_tree[end+1:]

  @staticmethod
  def parallel(behavior_tree):
    parallelSuccessCount = None
    if behavior_tree[1] != "/":
      sub_start = behavior_tree.find("/",1)+1
      parallelSuccessCount = int(behavior_tree[1:sub_start-1])
      #print "parallelSuccessCount:", parallelSuccessCount
    else:
      sub_start = 2

    opencount = 0;
    end = None
    for i in xrange(0,len(behavior_tree)):
      if re.match('/\d*/', behavior_tree[i:]):
        opencount += 1
        #print "opencount: ", opencount
      elif behavior_tree[i:i+2] == '\\\\':
        opencount -= 1
        #print "opencount: ", opencount
        if opencount is 0:
          end = i
          break

    if end is None:
      raise SyntaxWarning("End not found while parsing BT parallel node.\n"+behavior_tree)

    node = Node(
      NodeType.PARALLEL,
      children = Parser.parse(behavior_tree[sub_start:end])
    )
    if parallelSuccessCount is None: # must succed with all actions to succed in parallel
      node.parallelSuccessCount = len(node.children)
    else:
      node.parallelSuccessCount = parallelSuccessCount
    return node, behavior_tree[end+2:]


