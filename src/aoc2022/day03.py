import string
from collections.abc import Iterable, Iterator, Sequence
from itertools import chain
from typing import IO, TypeAlias

from more_itertools import chunked

from ._registry import register
from ._util import split

priorities = {
    letter: priority for priority, letter in enumerate(string.ascii_letters, 1)
}

Items: TypeAlias = Sequence[str]


def find_common(s: Iterable[Items]) -> set[str]:
    """Find items common to all batches"""
    first, *rest = s
    return set(first).intersection(*rest)


def compartments(rucksacks: Iterable[Items], n: int) -> Iterator[Iterable[Items]]:
    """Yield batches of items by splitting each rucksack into n compartments"""
    for rucksack in rucksacks:
        yield split(rucksack, n)


def sum_priorities(batches: Iterable[Iterable[Items]]) -> int:
    """Sum the priorities for the common items in each batch"""
    all_common = chain.from_iterable(find_common(batch) for batch in batches)
    return sum(priorities[item] for item in all_common)


@register(day=3)
def solve(file: IO[str], verbose: int) -> None:
    rucksacks = [line.strip() for line in file]

    print("Part 1:", sum_priorities(compartments(rucksacks, 2)))
    print("Part 2:", sum_priorities(chunked(rucksacks, 3, strict=True)))
