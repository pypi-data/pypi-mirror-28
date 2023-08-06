#!/usr/bin/env python3
# -*- coding: utf-8 -*-
#
#   Copyright 2018 Kaede Hoshikawa
#
#   Licensed under the Apache License, Version 2.0 (the "License");
#   you may not use this file except in compliance with the License.
#   You may obtain a copy of the License at
#
#       http://www.apache.org/licenses/LICENSE-2.0
#
#   Unless required by applicable law or agreed to in writing, software
#   distributed under the License is distributed on an "AS IS" BASIS,
#   WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
#   See the License for the specific language governing permissions and
#   limitations under the License.

from typing import Reversible, ItemsView, TypeVar, Generic, Tuple, \
    Any, Set, Iterable, Iterator, Union, AbstractSet

import typing
import collections

if typing.TYPE_CHECKING:  # pragma: no cover
    from ._frozen_dict import FrozenMagicDict  # noqa: F401

__all__ = ["MagicItemsView"]

_K = TypeVar("_K")

_V = TypeVar("_V")

_T = TypeVar("_T")


class MagicItemsView(
        Reversible[Tuple[_K, _V]], ItemsView[_K, _V], Generic[_K, _V]):
    __slots__ = ("_map",)

    def __init__(self, __map: "FrozenMagicDict[_K, _V]") -> None:
        self._map = __map

        super().__init__(self._map)  # type: ignore

    def _alter_keys_reduced(self, obj: Iterable[_T]) -> Set[Tuple[_K, Any]]:
        reduced_set: Set[Tuple[_K, Any]] = set()

        for i in obj:
            try:
                k, v = i  # type: ignore
                k = self._map._alter_key(k)

            except (AttributeError, TypeError):  # pragma: no cover
                continue

            reduced_set.add((k, v))

        return reduced_set

    def _maybe_alter_keys(self, obj: Iterable[_T]) -> Set[_T]:
        reduced_set: Set[_T] = set()

        for i in obj:
            try:
                k, v = i  # type: ignore
                k = self._map._maybe_alter_key(k)

            except (AttributeError, IndexError):  # pragma: no cover
                reduced_set.add(i)

            else:
                reduced_set.add((k, v))  # type: ignore

        return reduced_set

    def __iter__(self) -> Iterator[Tuple[_K, _V]]:
        for key, value in list(self._map._kv_pairs.values()):
            yield (key, value)

    def __contains__(self, pair: Any) -> bool:
        try:
            k, v = pair
            k = self._map._alter_key(k)

        except (AttributeError, IndexError):  # pragma: no cover
            return False

        return (k, v) in self._map._kv_pairs.values()

    def __eq__(self, obj: Any) -> bool:
        if not isinstance(obj, collections.abc.Iterable):  # pragma: no cover
            return False

        try:
            self_iter = iter(self)
            for k, v in obj:
                key, value = next(self_iter)

                if (key, value) != (self._map._maybe_alter_key(k), v):
                    return False

            else:
                try:
                    next(self_iter)

                except StopIteration:
                    return True

                else:
                    return False

        except (AttributeError, ValueError, TypeError, StopIteration):
            return False

    def __ne__(self, obj: Any) -> bool:
        return not self.__eq__(obj)

    def __lt__(self, obj: Iterable[Any]) -> bool:
        return super().__lt__(self._maybe_alter_keys(obj))

    def __le__(self, obj: Iterable[Any]) -> bool:
        return super().__le__(self._maybe_alter_keys(obj))

    def __gt__(self, obj: Iterable[Any]) -> bool:
        return super().__gt__(self._maybe_alter_keys(obj))

    def __ge__(self, obj: Iterable[Any]) -> bool:
        return super().__ge__(self._maybe_alter_keys(obj))

    def __and__(self, obj: Iterable[Any]) -> AbstractSet[Tuple[_K, _V]]:
        return super().__and__(self._alter_keys_reduced(obj))

    def __or__(
            self, obj: Iterable[_T]) -> AbstractSet[Union[Tuple[_K, _V], _T]]:
        return super().__or__(self._maybe_alter_keys(obj))

    def __sub__(self, obj: Iterable[Any]) -> AbstractSet[Tuple[_K, _V]]:
        return super().__sub__(self._alter_keys_reduced(obj))

    def __xor__(
            self, obj: Iterable[_T]) -> AbstractSet[Union[Tuple[_K, _V], _T]]:
        return super().__xor__(self._maybe_alter_keys(obj))

    def __reversed__(self) -> Iterator[Tuple[_K, _V]]:
        for key, value in reversed(  # type: ignore
                self._map._kv_pairs.values()):
            yield (key, value)
