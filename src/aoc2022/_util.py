from collections.abc import Iterable, Sequence
from typing import TypeVar

T = TypeVar("T")


def split(s: Sequence[T], n: int) -> Iterable[Sequence[T]]:
    """Split sequence into n groups"""
    grouplen = len(s) // n
    if grouplen * n != len(s):
        raise ValueError(f"sequence cannot be evenly split into {n} groups")

    for i in range(n):
        start = i * grouplen
        end = start + grouplen
        yield s[start:end]
