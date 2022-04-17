import pytest

from typing import Optional
from easy_fsm import AsyncStateMachine, AsyncState
from dataclasses import dataclass, field


@dataclass
class Stats:
    altitude: int = 0
    fly_time: int = 0
    suite: list[int] = field(default_factory=list)


class ComputeSyracuse(AsyncState[Stats]):
    def __init__(self, n: int):
        self.n = n

    async def run(self, context: Stats) -> Optional[AsyncState[Stats]]:
        context.altitude = max(context.altitude, self.n)
        context.fly_time += 1
        context.suite.append(self.n)

        if self.n == 1:
            return None

        elif self.n % 2 == 0:
            return ComputeSyracuse(self.n // 2)

        else:
            return ComputeSyracuse(3 * self.n + 1)


class Syracuse(AsyncStateMachine[Stats]):
    def __init__(self):
        super().__init__(Stats())

    async def compute(self, n: int) -> None:
        await self.run_from(ComputeSyracuse(n))


@pytest.mark.asyncio
async def test_fsm():
    fsm = Syracuse()
    await fsm.compute(5)

    assert fsm.context.altitude == 16
    assert fsm.context.fly_time == 6
    assert fsm.context.suite == [5, 16, 8, 4, 2, 1]
