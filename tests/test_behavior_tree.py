import unittest
from os.path import realpath, dirname
from ..behavior_tree import *

class TestBehaviorTree(unittest.TestCase):
  def setUp(self):
    pass

  def test_constructor(self):
    bt_file = BehaviorTree(None, dirname(realpath(__file__))+"/test.bt")
    bt = BehaviorTree(None, behavior_tree="""
      >
        one
        two
        ?
          three
          four
        !
      <
    """)
    self.assertRaises(AttributeError, BehaviorTree, None)

if __name__ == "__main__":
  unittest.main()