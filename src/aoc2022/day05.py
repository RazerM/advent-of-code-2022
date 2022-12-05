import re
from collections import defaultdict, deque
from collections.abc import Mapping
from copy import deepcopy
from operator import itemgetter
from typing import IO

from more_itertools import chunked

from ._registry import register


def move(
    stacks: Mapping[int, deque[str]],
    n: int,
    src: int,
    dest: int,
    *,
    preserve_order: bool = False,
) -> None:
    if preserve_order:
        buf: deque[str] = deque()
        for _ in range(n):
            buf.appendleft(stacks[src].pop())
        for _ in range(n):
            stacks[dest].append(buf.popleft())
    else:
        for _ in range(n):
            stacks[dest].append(stacks[src].pop())


@register(day=5)
def solve(file: IO[str], verbose: int) -> None:
    stacks: defaultdict[int, deque[str]] = defaultdict(deque)
    instructions = []
    for line in file:
        if line.startswith("["):
            for i, crate in enumerate(map(itemgetter(1), chunked(line, 4)), 1):
                if crate.isalpha():
                    stacks[i].appendleft(crate)
        elif match := re.match(r"move (\d+) from (\d+) to (\d+)", line):
            n, src, dest = map(int, match.groups())
            instructions.append((n, src, dest))

    stacks1 = deepcopy(stacks)
    stacks2 = deepcopy(stacks)
    for n, src, dest in instructions:
        move(stacks1, n, src, dest)
        move(stacks2, n, src, dest, preserve_order=True)

    print("Part 1:", "".join(stacks1[key][-1] for key in sorted(stacks1)))
    print("Part 2:", "".join(stacks2[key][-1] for key in sorted(stacks2)))
