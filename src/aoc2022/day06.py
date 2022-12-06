from typing import IO

from ._registry import register


def find_marker(stream: str, n: int) -> int:
    for i in range(len(stream)):
        if len(set(stream[max(0, i - n) : i])) == n:
            return i


@register(day=6)
def solve(file: IO[str], verbose: int) -> None:
    stream = file.read().strip()
    print("Part 1:", find_marker(stream, 4))
    print("Part 2:", find_marker(stream, 14))
