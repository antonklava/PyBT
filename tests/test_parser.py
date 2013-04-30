import unittest
from ..parser import Parser
from ..node import NodeType

class TestParser(unittest.TestCase):
  def setUp(self):
    pass

  def test_parse_one_action(self):
    root = Parser.parse("""
      action
      """)[0]
    assert(root.type == NodeType.ACTION_CONDITION)
    assert(root.action == "action")

  def test_fail_action(self):
    self.assertRaises(SyntaxWarning, Parser.parse, """
      on_"!#e
      """)

  def test_parse_two_actions(self):
    roots = Parser.parse("""
      one
      two
      """)
    assert(len(roots)==2)
    assert(roots[0].type == NodeType.ACTION_CONDITION)
    assert(roots[1].type == NodeType.ACTION_CONDITION)
    assert(roots[0].action == "one")
    assert(roots[1].action == "two")

  def test_simple_sequence(self):
    root = Parser.parse("""
      >
        one
      <
      """)[0]
    self.assertIs(root.type, NodeType.SEQUENCE)
    self.assertIs(len(root.children), 1)
    self.assertIs(root.children[0].type, NodeType.ACTION_CONDITION)

  def test_fail_sequence(self):
    self.assertRaises(SyntaxWarning, Parser.parse, """
      >
        one
      """)

  def test_two_sequences(self):
    roots = Parser.parse("""
      >
        one
      <
      >
        two
      <
      """)
    for i in xrange(0,2):
      self.assertIs(roots[i].type, NodeType.SEQUENCE)
      self.assertIs(len(roots[i].children), 1)
      self.assertIs(roots[i].children[0].type, NodeType.ACTION_CONDITION)

  def test_nested_sequences(self):
    root = Parser.parse("""
      >
        >
          two
        <
      <
      """)[0]
    assert(root.type == NodeType.SEQUENCE)
    assert(root.children[0].type == NodeType.SEQUENCE)
    assert(root.children[0].children[0].type == NodeType.ACTION_CONDITION)

  def test_prio(self):
    root = Parser.parse("""
      ?
        one
      !
    """)[0]
    assert(root.type == NodeType.PRIORITY)
    assert(len(root.children) == 1)
    assert(root.children[0].type == NodeType.ACTION_CONDITION)
    assert(root.children[0].action == "one")

  def test_two_prio(self):
    roots = Parser.parse("""
      ?
        one
      !
      ?
        two
      !
      """)
    for i in xrange(0,2):
      self.assertIs(roots[i].type, NodeType.PRIORITY)
      self.assertIs(len(roots[i].children), 1)
      self.assertIs(roots[i].children[0].type, NodeType.ACTION_CONDITION)

  def test_nested_prio(self):
    root = Parser.parse("""
      ?
        ?
          two
        !
      !
      """)[0]
    assert(root.type == NodeType.PRIORITY)
    assert(root.children[0].type == NodeType.PRIORITY)
    assert(root.children[0].children[0].type == NodeType.ACTION_CONDITION)

  def test_fail_prio(self):
    self.assertRaises(SyntaxWarning, Parser.parse, """
      ?
        one
      """)

  def test_simple_parallel(self):
    root = Parser.parse("""
      //
        one
        two
      \\\\
      """)[0]
    assert root.type == NodeType.PARALLEL
    assert len(root.children) == 2
    assert root.parallelSuccessCount == 2

  def test_simple_parallel_with_success_count(self):
    root = Parser.parse("""
      /1/
        one
        two
      \\\\
      """)[0]
    assert root.type == NodeType.PARALLEL
    assert len(root.children) == 2
    assert root.parallelSuccessCount == 1

  def test_two_parallel(self):
    roots = Parser.parse("""
      /1/
        one
        two
      \\\\
      //
        one
        two
      \\\\
      """)
    assert roots[0].type == NodeType.PARALLEL
    assert roots[1].type == NodeType.PARALLEL
    assert len(roots[0].children) == 2
    assert len(roots[1].children) == 2
    assert roots[0].parallelSuccessCount == 1
    assert roots[1].parallelSuccessCount == 2

  def test_parse_full(self):
    root = Parser.parse("""
      >
        one
        two
        ?
          three
          four
        !
        /2/
          parallelone
          paralleltwo
        \\\\
        //
          parallelthree
          parallelfour
        \\\\
        # dat comment
        ?
          five
          six
        !
        # moar comments
      <
    """)[0]
    assert(root.type == NodeType.SEQUENCE)

if __name__ == "__main__":
  unittest.main()