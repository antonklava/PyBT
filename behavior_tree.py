from .parser import Parser

class BehaviorTree:
  """
  BehaviorTree (BT) implementation.

  Calls methods on actor with same name as actions and conditions in the behavior tree.

  ? ... !     - Priority (Until one success)
  > ... <     - Sequence (All success)
  /n/ ... \\  - Parallel (n successful or more, default all)

  written by Anton Klava, aklava@kth.se
  27 Apr 2013 - 20:50
  """
  def __init__(self, actor, filename=None, behavior_tree=None):
    if filename is not None:
      behavior_tree = open(filename, 'r').read()

    if behavior_tree is "" or behavior_tree is None:
      raise AttributeError('Could not get behavior tree from file or string.')

    self.actor = actor
    self.behavior_tree = Parser.parse(behavior_tree)
