import operator
from collections import defaultdict
from collections.abc import Iterable, Sequence
from functools import reduce
from typing import IO, TypeVar

from ._registry import register

T = TypeVar("T")


def viewing_distance(trees: Iterable[int], height: int) -> int:
    seen = 0
    for i, tree in enumerate(trees):
        if tree < height:
            seen += 1
        elif tree >= height:
            seen += 1
            break
    return seen


def before(seq: Sequence[T], i: int) -> Sequence[T]:
    return seq[:i][::-1]


def after(seq: Sequence[T], i: int) -> Sequence[T]:
    return seq[i + 1 :]


@register(day=8)
def solve(file: IO[str], verbose: int) -> None:
    grid = dict()
    columns = defaultdict(list)
    rows = dict()
    for y, line in enumerate(file):
        row = [int(h) for h in line.rstrip()]
        rows[y] = row
        for x, height in enumerate(row):
            grid[x, y] = height
            columns[x].append(height)

    num_visible = 0
    max_score = 0
    for (x, y), height in grid.items():
        row = rows[y]
        col = columns[x]

        up = before(col, y)
        left = before(row, x)
        down = after(col, y)
        right = after(row, x)

        directions = [up, left, down, right]

        num_visible += any(all(h < height for h in trees) for trees in directions)
        viewing_distances = (viewing_distance(trees, height) for trees in directions)
        score = reduce(operator.mul, viewing_distances)
        max_score = max(max_score, score)

    print("Part 1:", num_visible)
    print("Part 2:", max_score)
