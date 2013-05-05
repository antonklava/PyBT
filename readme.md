# PyBT
A lightweight [behavior tree](http://www.altdevblogaday.com/2011/02/24/introduction-to-behavior-trees/) implementation in python.

## How to use it
Clone this repo and make sure the pybt package folder is in your PYTHONPATH environment variable. Try with `import pybt` to make sure it can be found.

- *BehaviorTree class* - is the implementation of the actual behavior tree. Here the nodes
are traversed and the actions/conditions called.
- *Actor class* - A class that should be extended to run the actions and conditions of the behavior tree.
- *Status class* - More of an enum really (Status.SUCCESS, Status.RUNNING, Status.FAIL). Have to be returned by every action/condition in the actor class.
- *BehaviorTree tick* - The behavior tree has to be 'ticked' to call actions/conditions. This may be done for example once every update loop.

## Writing behavior trees
Behavior trees can be supplied by passing a string or a filename when creating the BehaviorTree class.

### Actions/conditions
Actions and conditions should be written on its own line. Underscores in action/condition-names are allowed.

    my_first_action
    my_second_action

### Sequence
The sequence selector starts with a `>` and ends with `<`. Every action/conditon or other node inside the sequence selector runs one after another, from the top, until one returns Status.FAIL.

    >
      my_first_action
      my_second_action
    <

### Priority
The priority selector starts with a `?` and ends with `!`. Every action/condition or other node inside the priority selector runs one after another, from the top, until one returns Status.SUCCESS

    ?
      my_first_action
      my_second_action
    !

### Parallel
The parallel selector starts with a `//` or `/n/` and ends with `\\`. The number **n** decides how many actions/conditions/nodes inside the parallel selector that atleast must return success for the parallel node to return success. If **n** is not provided every action/condition or other node must succeed for the parallel node to succeed. Every action/condition or other node inside the parallel selector is ticked once and then the response is examined.

    //
      my_first_action
      my_second_action
    \\

### Comments
Lines starting with `#` will be ignored.

    # This is a comment

### Importing subtrees/files
Importing other trees from files is also supported. File imports should be done on a new line and with the file path starting with `:`

    :my_behavior_trees/behavior_tree.bt

## Example
This simple example first defines an actor class MyActor with some actions and conditions. Then a behavior tree is created. The root node in the tree is a priority node, which will stop only when an action/condition/node has succeeded. It first checks if too much time as passed, wich in the first 3 seconds has not and therefore returns Status.FAIL. The priority node tries the sequence node. The sequence node will return success if all actions/conditions/nodes in it returns success. This will not happen until enough_time_has_passed returns true - after 1.5 seconds. After this time the condition returns true and my_action is called printing "My Action was called!" until too_much_time_has_passed starts returning success - after another 1.5 seconds.

    from pybt.behavior_tree import BehaviorTree, Status
    from pybt.actor import Actor

    from time import time, sleep

    class MyActor(Actor):
      """My actor implementation. Runs the actions/conditions from my behavior tree!"""
      def __init__(self):
        Actor.__init__(self)
        self.time = time()

      def my_action(self, state):
        print "My Action was called!"
        return Status.SUCCESS

      def enough_time_has_passed(self, state):
        if (time()-self.time) > 1.5:
          return Status.SUCCESS
        return Status.FAIL

      def too_much_time_has_passed(self, state):
        if (time()-self.time) > 3:
          return Status.SUCCESS
        return Status.FAIL

    if __name__=="__main__":
      # Behavior tree may also be supplied as a file
      # bt = BehaviorTree(MyActor(), "my_behavior_tree.bt")
      bt = BehaviorTree(MyActor(), behavior_tree="""
        ?
          too_much_time_has_passed
          >
            enough_time_has_passed
            my_action
          <
        !
        """)
      while True:
        print "Tick tock"
        bt.tick() # You may supply a state object in the tick method that
                  # is passwed to all actions as a parameter. Default: None
        sleep(0.5)

## Running the tests
Easiest way to run all tests is with [nose](https://nose.readthedocs.org/en/latest/).

    nosetests pybt

You can also run individual test suits.

    python -m pybt.tests.test_parser

Can also be nice to run specific test cases

    python -m pybt.tests.test_parser TestParser.test_nested_prio

## Contributing
Write some code with test and make a pull request! Any additions are welcome!

## TODO
- Graphical representation of the tree
- Behavior tree runner (no need to provide custom loop)
