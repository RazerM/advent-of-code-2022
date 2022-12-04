from collections.abc import Set
from typing import IO, TypeAlias

from ._registry import register

Range: TypeAlias = Set[int]


def parse_pair(s: str) -> tuple[Range, Range]:
    a, b = s.strip().split(",")
    return parse_range(a), parse_range(b)


def parse_range(s: str) -> Range:
    start, end = map(int, s.split("-"))
    return set(range(start, end + 1))


@register(day=4)
def solve(file: IO[str], verbose: int) -> None:
    num_subsets = 0
    num_overlaps = 0
    for line in file:
        a, b = parse_pair(line)

        if a <= b or a >= b:
            num_subsets += 1
            num_overlaps += 1
        elif not a.isdisjoint(b):
            num_overlaps += 1

    print("Part 1:", num_subsets)
    print("Part 2:", num_overlaps)
