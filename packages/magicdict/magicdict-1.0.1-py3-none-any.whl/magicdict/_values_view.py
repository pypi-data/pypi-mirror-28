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

from typing import ValuesView, Generic, Iterator, Any, TypeVar

import typing

if typing.TYPE_CHECKING:  # pragma: no cover
    from ._frozen_dict import FrozenMagicDict  # noqa: F401

__all__ = ["MagicValuesView"]

_V = TypeVar("_V")

_T = TypeVar("_T")


class MagicValuesView(ValuesView[_V], Generic[_V]):
    __slots__ = ("_map",)

    def __init__(self, __map: "FrozenMagicDict[Any, _V]") -> None:
        self._map = __map

        super().__init__(self._map)  # type: ignore

    def __iter__(self) -> Iterator[_V]:
        for _, value in self._map._kv_pairs.values():
            yield value

    def __contains__(self, value: Any) -> bool:
        for _, _value in self._map._kv_pairs.values():
            if _value == value:
                return True

        else:
            return False

    def __reversed__(self) -> Iterator[_V]:
        for _, value in reversed(self._map._kv_pairs.values()):  # type: ignore
            yield value
