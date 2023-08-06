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

from typing import \
    Iterator, KeysView, Generic, Union, Iterable, Set, Any, Reversible, \
    TypeVar, AbstractSet

import typing
import collections

if typing.TYPE_CHECKING:  # pragma: no cover
    from ._frozen_dict import FrozenMagicDict  # noqa: F401

__all__ = ["MagicKeysView"]

_K = TypeVar("_K")

_T = TypeVar("_T")


class MagicKeysView(KeysView[_K], Reversible[_K], Generic[_K]):
    __slots__ = ("_map",)

    def __init__(self, __map: "FrozenMagicDict[_K, Any]") -> None:
        self._map = __map

        super().__init__(self._map)  # type: ignore

    def _alter_keys_reduced(self, obj: Iterable[_T]) -> Set[_T]:
        reduced_set: Set[_T] = set()

        for i in obj:
            try:
                i = self._map._alter_key(i)  # type: ignore

            except (AttributeError, TypeError):  # pragma: no cover
                continue

            reduced_set.add(i)

        return reduced_set

    def _maybe_alter_keys(self, obj: Iterable[_T]) -> Set[_T]:
        reduced_set: Set[_T] = set()

        for i in obj:
            try:
                i = self._map._maybe_alter_key(i)

            except (AttributeError, TypeError):  # pragma: no cover
                pass

            reduced_set.add(i)

        return reduced_set

    def __contains__(self, key: Any) -> bool:
        return self._map._maybe_alter_key(key) in self._map._pair_ids.keys()

    def __eq__(self, obj: Any) -> bool:
        if not isinstance(obj, collections.abc.Iterable):  # pragma: no cover
            return False

        try:
            self_iter = iter(self)
            for val in obj:
                key = next(self_iter)

                if key != self._map._maybe_alter_key(val):
                    return False

            else:
                try:
                    next(self_iter)

                except StopIteration:
                    return True

                else:
                    return False

        except (AttributeError, TypeError, StopIteration):  # pragma: no cover
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

    def __and__(self, obj: Iterable[Any]) -> AbstractSet[_K]:
        return super().__and__(self._alter_keys_reduced(obj))

    def __or__(self, obj: Iterable[_T]) -> AbstractSet[Union[_K, _T]]:
        return super().__or__(self._maybe_alter_keys(obj))

    def __sub__(self, obj: Iterable[Any]) -> AbstractSet[_K]:
        return super().__sub__(self._alter_keys_reduced(obj))

    def __xor__(self, obj: Iterable[_T]) -> AbstractSet[Union[_K, _T]]:
        return super().__xor__(self._maybe_alter_keys(obj))

    def __reversed__(self) -> Iterator[_K]:
        for key, _ in reversed(self._map._kv_pairs.values()):  # type: ignore
            yield key
