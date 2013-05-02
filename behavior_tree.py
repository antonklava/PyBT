from .parser import Parser
from .node import NodeType

class Status:
  SUCCESS = 1
  RUNNING = 2
  FAIL    = 3
  @staticmethod
  def str(status):
    return ["SUCCESS", "RUNNING", "FAIL"][status-1]

class BehaviorTree:
  """
  BehaviorTree (BT) implementation.

  Calls methods on actor with same name as actions and conditions in the behavior tree.
  """
  def __init__(self, actor, filename=None, behavior_tree=None):
    if filename is not None:
      behavior_tree = open(filename, 'r').read()
    if behavior_tree is "" or behavior_tree is None:
      raise AttributeError('Could not get behavior tree from file or string.')
    self.actor = actor
    self.root = Parser.parse(behavior_tree)[0] # only takes the first node

  def tick(self, state = None):
    return self.tick_node(self.root, state)

  def tick_node(self, node, state):
    if node.type in [ NodeType.ACTION,
                      NodeType.CONDITION,
                      NodeType.ACTION_CONDITION ]:
      return self.action_condition(node, state)
    elif node.type == NodeType.SEQUENCE:
      return self.sequence(node, state)
    elif node.type == NodeType.PRIORITY:
      return self.priority(node, state)
    elif node.type == NodeType.PARALLEL:
      return self.parallel(node, state)

  def action_condition(self, node, state):
    #print "Action node",node,":"
    response = self.actor.run_action(node.action, state)
    #print Status.str(response)
    return response

  def sequence(self, node, state):
    #print "Sequence node", node
    for child in node.children:
      #print "Ticking child node: ", child
      response = self.tick_node(child, state)
      if response in [Status.RUNNING, Status.FAIL]:
        #print "child node", node, " ", Status.str(response)
        return response
    return Status.SUCCESS

  def priority(self, node, state):
    #print "Priority node", node
    for child in node.children:
      #print "Ticking child node: ", child
      response = self.tick_node(child, state)
      if response in [Status.RUNNING, Status.SUCCESS]:
        #print "child node", node, " ", Status.str(response)
        return response
    return Status.FAIL

  def parallel(self, node, state):
    #print "Parallel node", node
    responses = []
    for child in node.children:
      responses.append(self.tick_node(child, state))
    if responses.count(Status.RUNNING) == len(responses):
      return Status.RUNNING
    elif responses.count(Status.SUCCESS) >= node.parallelSuccessCount:
      return Status.SUCCESS
    else:
      return Status.FAIL

