from collections.abc import Iterable, Iterator, MutableSet
from typing import Generic, TypeVar

_T = TypeVar("_T")


class OrderedSet(MutableSet[_T]):
    "only works on python >=3.6"
    __slots__ = ["_inner"]

    def __init__(self, *args: _T) -> None:
        self._inner: dict[_T, None] = dict.fromkeys(args)

    def __iter__(self) -> Iterator[_T]:
        return self._inner.keys().__iter__()

    def __len__(self) -> int:
        return len(self._inner)

    def __contains__(self, value) -> bool:
        return value in self._inner
