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

from typing import TypeVar, Generic, AnyStr, Any

from ._frozen_dict import FrozenMagicDict

_V = TypeVar("_V")

__all__ = ["FrozenTolerantMagicDict"]


class FrozenTolerantMagicDict(
        FrozenMagicDict[AnyStr, _V], Generic[AnyStr, _V]):
    """
    `FrozenTolerantMagicDict` has exactly the same functionality as
    `FrozenMagicDict`. However, the keys are case-insensitive.
    """
    __slots__ = ()

    @staticmethod
    def _alter_key(key: AnyStr) -> AnyStr:
        return key.lower()

    @staticmethod
    def _maybe_alter_key(key: Any) -> Any:
        if isinstance(key, (str, bytes)):
            return key.lower()

        return key

    def copy(self) -> "FrozenTolerantMagicDict[AnyStr, _V]":
        return self.__class__(self)
