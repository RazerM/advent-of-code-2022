import re
from collections import deque
from collections.abc import Iterator, MutableMapping
from os import PathLike
from pathlib import PurePosixPath
from typing import IO, TYPE_CHECKING, TypeAlias, cast

from attrs import Factory, define, field

from ._registry import register

if TYPE_CHECKING:
    DirectoryMapping: TypeAlias = "MutableMapping[str, File | Directory]"
else:
    DirectoryMapping = MutableMapping


@define
class File:
    size: int


@define
class Directory(DirectoryMapping):
    entries: "dict[str, File | Directory]" = Factory(dict)
    _cached_size: int | None = field(init=False, default=None)

    def __getitem__(self, key: str) -> "File | Directory":
        return self.entries[key]

    def get_path(self, path: str | PathLike[str]) -> "File | Directory":
        path = PurePosixPath(path)
        file_or_dir: "File | Directory" = self
        for i, part in enumerate(path.parts):
            if not isinstance(file_or_dir, Directory):
                subpath = PurePosixPath(*path.parts[:i])
                raise ValueError(f"{subpath} is not a directory")
            file_or_dir = file_or_dir[part]
        return file_or_dir

    def __setitem__(self, key: str, value: "File | Directory") -> None:
        self.entries[key] = value

    def __delitem__(self, key: str) -> None:
        del self.entries[key]

    def __iter__(self) -> Iterator[str]:
        return iter(self.entries)

    def __len__(self) -> int:
        return len(self.entries)

    def compute_size(self, *, refresh: bool = True) -> int:
        if self._cached_size is not None and not refresh:
            return self._cached_size

        size = 0
        for name, entry in self.items():
            if isinstance(entry, File):
                size += entry.size
            elif isinstance(entry, Directory):
                size += entry.compute_size()
            else:
                raise RuntimeError(f"Unhandled entry: {entry}")

        self._cached_size = size
        return size

    def directories(
        self, *, recursive: bool = False
    ) -> "Iterator[tuple[str, Directory]]":
        queue = deque([self])
        while queue:
            dir_ = queue.popleft()
            for name, entry in dir_.items():
                if isinstance(entry, Directory):
                    if recursive:
                        queue.append(entry)
                    yield name, entry


@register(day=7)
def solve(file: IO[str], verbose: int) -> None:
    cwd = PurePosixPath("/")

    root = Directory()
    fs = Directory({"/": root})
    in_command = None
    cwd_fs: Directory = root

    for line in file:
        line = line.rstrip()
        if line.startswith("$"):
            in_command = None
            args = line.removeprefix("$").lstrip().split()
            match args:
                case ["cd", "/"]:
                    cwd = PurePosixPath("/")
                    cwd_fs = root
                case ["cd", ".."]:
                    cwd = cwd.parent
                    cwd_fs = cast(Directory, fs.get_path(cwd))
                case ["cd", x]:
                    cwd /= x
                    file_or_dir = fs.get_path(cwd)
                    assert isinstance(file_or_dir, Directory)
                    cwd_fs = file_or_dir
                case ["ls"]:
                    in_command = "ls"
                case _:
                    raise RuntimeError(f"Unhandled command: {line}")
        elif in_command == "ls":
            if match := re.match(r"dir\s+(.+)", line):
                dir_ = match[1]
                cwd_fs[dir_] = Directory()
            elif match := re.match(r"(\d+)\s+(.+)", line):
                size = int(match[1])
                filename = match[2]
                cwd_fs[filename] = File(size=size)
            else:
                raise RuntimeError(f"Unhandled ls: {line}")

    total = fs.compute_size()
    disk_space = 70_000_000
    need_unused = 30_000_000
    free = disk_space - total

    sizes = [
        dir_.compute_size(refresh=False) for _, dir_ in fs.directories(recursive=True)
    ]

    print("Part 1:", sum(size for size in sizes if size <= 100_000))
    print("Part 2:", min(size for size in sorted(sizes) if size + free >= need_unused))
