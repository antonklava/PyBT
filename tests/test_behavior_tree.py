import unittest
from os.path import realpath, dirname
from ..behavior_tree import BehaviorTree, Status
from ..actor import Actor

class CountActor(Actor):
  call_count = 0
  def success(self, status):
    self.call_count += 1
    return Status.SUCCESS

  def fail(self, status):
    self.call_count += 1
    return Status.FAIL

class TestBehaviorTree(unittest.TestCase):
  def setUp(self):
    self.actor = CountActor()
    self.very_simple_tree = """
    >
      one
    <
    """
    self.simple_tree = """
      >
        one
        two
        ?
          three
          four
        !
      <
    """
    self.simple_parallel = """
    >
      /1/
        success
        fail
      \\\\
      success
    <
    """

  def test_constructor(self):
    bt_file = BehaviorTree(None, dirname(realpath(__file__))+"/test.bt")
    bt = BehaviorTree(None, behavior_tree=self.simple_tree)
    self.assertRaises(AttributeError, BehaviorTree, None)

  def test_very_simple_tick(self):
    class TmpActor(Actor):
      self.called = False
      def one(self, state):
        self.called = True
        return Status.SUCCESS
    actor = TmpActor()
    bt = BehaviorTree(actor, behavior_tree=self.very_simple_tree)
    bt.tick(None)
    assert actor.called

  def test_simple_tick(self):
    class TmpActor(Actor):
      called = False
      def one(self, status):
        return Status.SUCCESS
      def two(self, status):
        return Status.SUCCESS
      def three(self, status):
        return Status.FAIL
      def four(self, status):
        self.called = True
        return Status.SUCCESS
    actor = TmpActor()
    bt = BehaviorTree(actor, behavior_tree=self.simple_tree)
    bt.tick(None)
    assert actor.called

  def test_simple_parallel(self):
    bt = BehaviorTree(self.actor, behavior_tree=self.simple_parallel)
    bt.tick(None)
    assert self.actor.call_count == 3

  def test_sequence_fail(self):
    bt = BehaviorTree(self.actor, behavior_tree="""
      >
        success
        fail
        success
      <
      """) # should abort after fail
    bt.tick(None)
    assert self.actor.call_count == 2

  def test_prio_fail(self):
    bt = BehaviorTree(self.actor, behavior_tree="""
      ?
        success
        fail
        success
      !
      """) # should abort after success
    bt.tick(None)
    assert self.actor.call_count == 1

if __name__ == "__main__":
  unittest.main()