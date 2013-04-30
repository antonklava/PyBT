class NodeType:
  ACTION = 1
  CONDITION = 2
  ACTION_CONDITION = 3
  PRIORITY = 3
  SEQUENCE = 4
  PARALLEL = 5

  @staticmethod
  def str(nodeType):
    return [
      "ACTION",
      "CONDITION",
      "ACTION_CONDITION",
      "PRIORITY",
      "SEQUENCE",
      "PARALLEL"
    ][nodeType]

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
    return "[{}:{}:{}]".format(
      NodeType.str(self.type),
      NodeType.str(self.parent.type) if self.parent is not None else "_",
      len(self.children)
    )
