from collections.abc import Iterator
from enum import Enum
from functools import total_ordering
from typing import IO, Any

from ._registry import register


class Result(Enum):
    LOSE = "X"
    DRAW = "Y"
    WIN = "Z"


@total_ordering
class Shape(Enum):
    ROCK = 1
    PAPER = 2
    SCISSORS = 3

    @classmethod
    def decrypt_opponent(cls, value: str) -> "Shape":
        match value:
            case "A":
                return cls.ROCK
            case "B":
                return cls.PAPER
            case "C":
                return cls.SCISSORS
            case _:
                raise ValueError(f"Unknown shape: {value}")

    @classmethod
    def decrypt_response(cls, value: str) -> "Shape":
        """In part 1 we assume these values indicate which shape to play"""
        match value:
            case "X":
                return cls.ROCK
            case "Y":
                return cls.PAPER
            case "Z":
                return cls.SCISSORS
            case _:
                raise ValueError(f"Unknown shape: {value}")

    def __gt__(self, other: Any) -> bool:
        if type(other) is not Shape:
            return NotImplemented

        match self, other:
            case Shape.ROCK, Shape.SCISSORS:
                return True
            case Shape.PAPER, Shape.ROCK:
                return True
            case Shape.SCISSORS, Shape.PAPER:
                return True
            case _:
                return False

    def beat(self) -> "Shape":
        return next(shape for shape in Shape if shape > self)

    def beats(self) -> "Shape":
        return next(shape for shape in Shape if shape < self)

    def score(self, other: "Shape") -> int:
        if self > other:
            return self.value + 6
        elif self == other:
            return self.value + 3
        else:
            return self.value


def play_assumed_response(guide: list[list[str]]) -> Iterator[int]:
    for a, b in guide:
        opponent = Shape.decrypt_opponent(a)
        response = Shape.decrypt_response(b)
        yield response.score(opponent)


def play_strategy(guide: list[list[str]]) -> Iterator[int]:
    for a, b in guide:
        opponent = Shape.decrypt_opponent(a)
        result = Result(b)
        match result:
            case Result.DRAW:
                response = opponent
            case Result.WIN:
                response = opponent.beat()
            case Result.LOSE:
                response = opponent.beats()
            case _:
                raise RuntimeError(f"unhandled: {result}")

        yield response.score(opponent)


@register(day=2)
def solve(file: IO[str], verbose: int) -> None:
    guide = [line.strip().split() for line in file]
    print("Part 1:", sum(play_assumed_response(guide)))
    print("Part 2:", sum(play_strategy(guide)))
