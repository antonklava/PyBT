from .behavior_tree import Status
class Actor:
  """
    Actor superclass
    Calls methods with same name as actions in run_actions
  """
  def __init__(self):
    pass

  def run_action(self, action, state):
    f = getattr(self, action)
    if not f:
      raise NotImplementedError("Action '"+action+"' was not implemented in actor.")
    response = f(state)
    if not response in [Status.SUCCESS, Status.RUNNING, Status.FAIL]:
      raise ValueError("Action '"+action+"' did not return expected Status response.\n"+response)
    return response