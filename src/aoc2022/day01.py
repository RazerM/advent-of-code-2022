from collections.abc import Iterable
from operator import not_
from typing import IO, cast

from more_itertools import split_at

from ._registry import register


@register(day=1)
def solve(file: IO[str], verbose: int) -> None:
    lines = (line.strip() for line in file)
    numbers = (int(line) if line else None for line in lines)
    elves = cast("Iterable[list[int]]", split_at(numbers, not_))
    sorted_totals = sorted((sum(elf) for elf in elves), reverse=True)

    print("Part 1:", sorted_totals[0])
    print("Part 2:", sum(sorted_totals[:3]))
