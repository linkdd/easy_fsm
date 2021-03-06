easy_fsm
========

Easy to implement Finite State Machines.

.. image:: https://img.shields.io/pypi/l/easy_fsm.svg?style=flat-square
   :target: https://pypi.python.org/pypi/easy_fsm/
   :alt: License

.. image:: https://img.shields.io/pypi/status/easy_fsm.svg?style=flat-square
   :target: https://pypi.python.org/pypi/easy_fsm/
   :alt: Development Status

.. image:: https://img.shields.io/pypi/v/easy_fsm.svg?style=flat-square
   :target: https://pypi.python.org/pypi/easy_fsm/
   :alt: Latest release

.. image:: https://img.shields.io/pypi/pyversions/easy_fsm.svg?style=flat-square
   :target: https://pypi.python.org/pypi/easy_fsm/
   :alt: Supported Python versions

.. image:: https://img.shields.io/pypi/implementation/easy_fsm.svg?style=flat-square
   :target: https://pypi.python.org/pypi/easy_fsm/
   :alt: Supported Python implementations

.. image:: https://img.shields.io/pypi/wheel/easy_fsm.svg?style=flat-square
   :target: https://pypi.python.org/pypi/easy_fsm
   :alt: Download format

.. image:: https://img.shields.io/github/workflow/status/linkdd/easy_fsm/run-test-suite?style=flat-square
   :target: https://github.com/linkdd/easy_fsm/actions/workflows/test-suite.yml
   :alt: Build Status

.. image:: https://img.shields.io/pypi/dm/easy_fsm.svg?style=flat-square
   :target: https://pypi.python.org/pypi/easy_fsm/
   :alt: Downloads

Introduction
------------

**easy_fsm** provides a very simple API to build finite state machines.

The state machine holds a context that is passed to the different states.

Each state returns either the next state to execute or `None` if the execution
is done.

This allows you to implement business logic in small, well separated, chunks of
code.

Example
-------

.. code-block:: python

   from typing import Optional
   from easy_fsm import StateMachine, State
   from dataclasses import dataclass, field


   @dataclass
   class Stats:
       altitude: int = 0
       fly_time: int = 0
       suite: list[int] = field(default_factory=list)


   class ComputeSyracuse(State[Stats]):
       def __init__(self, n: int):
           self.n = n

       def run(self, context: Stats) -> Optional[State[Stats]]:
           context.altitude = max(context.altitude, self.n)
           context.fly_time += 1
           context.suite.append(self.n)

           if self.n == 1:
               return None

           elif self.n % 2 == 0:
               return ComputeSyracuse(self.n // 2)

           else:
               return ComputeSyracuse(3 * self.n + 1)


   class Syracuse(StateMachine[Stats]):
       def __init__(self):
           super().__init__(Stats())

       def compute(self, n: int) -> None:
           self.run_from(ComputeSyracuse(n))


   def test_fsm():
       fsm = Syracuse()
       fsm.compute(5)

       assert fsm.context.altitude == 16
       assert fsm.context.fly_time == 6
       assert fsm.context.suite == [5, 16, 8, 4, 2, 1]


License
-------

This project is released under the terms of the `MIT License`_.

.. _MIT License: https://github.com/linkdd/easy_fsm/blob/main/LICENSE.txt
