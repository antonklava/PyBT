class NodeType:
  ACTION = 1
  CONDITION = 2
  ACTION_CONDITION = 3
  PRIORITY = 4
  SEQUENCE = 5
  PARALLEL = 6

  @staticmethod
  def str(nodeType):
    return [
      "ACTION",
      "CONDITION",
      "ACTION_CONDITION",
      "PRIORITY",
      "SEQUENCE",
      "PARALLEL"
    ][nodeType-1]

class Node:
  """
  BehaviorTree node

  parnet    - Node or None
  children  - Nodes or []
  type      - NodeType
  """
  def __init__(self, type_, children=[], parent=None, action=None, parallelSuccessCount=None):
    if type_ is None:
      raise AttributeError("Must set type in Node")
    self.type                 = type_
    self.parent               = parent
    self.children             = children
    self.action               = action
    self.parallelSuccessCount = parallelSuccessCount

  def __str__(self):
    if self.type in [NodeType.ACTION, NodeType.CONDITION, NodeType.ACTION_CONDITION]:
      selfstr = "{}({})".format(NodeType.str(self.type), self.action)
    else:
      selfstr = NodeType.str(self.type)

    return "[{}:{}:{}]".format(
      selfstr,
      NodeType.str(self.parent.type) if self.parent is not None else "_",
      len(self.children)
    )
