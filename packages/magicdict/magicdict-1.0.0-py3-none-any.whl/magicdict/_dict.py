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

from typing import MutableMapping, Generic, TypeVar, Any, Union, Tuple

from ._frozen_dict import FrozenMagicDict

import threading
import collections

__all__ = ["MagicDict"]

_K = TypeVar("_K")

_V = TypeVar("_V")

_T = TypeVar("_T")


class _Identifier:
    pass


_DEFAULT_MARK = _Identifier()


class MagicDict(
        FrozenMagicDict[_K, _V], MutableMapping[_K, _V], Generic[_K, _V]):
    """
    A mutable version of `FrozenMagicDict`.
    """
    __slots__ = ("_lock",)

    def __init__(self, *args: Any, **kwargs: Any) -> None:
        self._lock = threading.Lock()

        super().__init__(*args, **kwargs)

    def _add_one(self, key: _K, value: _V) -> None:
        with self._lock:
            super()._add_one(key, value)

    def __setitem__(self, key: _K, value: _V) -> None:
        key = self._alter_key(key)

        with self._lock:
            index = self._get_next_index()

            self._first_values[key] = value

            self._pair_ids[key] = [index]
            self._kv_pairs[index] = (key, value)

            self._last_values[key] = value

    def __delitem__(self, key: _K) -> None:
        key = self._alter_key(key)

        with self._lock:
            del self._first_values[key]

            indexes = self._pair_ids.pop(key)
            for index in indexes:
                del self._kv_pairs[index]

            del self._last_values[key]

    def add(self, key: _K, value: _V) -> None:
        """
        Add a value corresponding to the key without removing the former one.
        """
        self._add_one(key, value)

    def pop(
        self, key: _K, default: Union[_V, _T, _Identifier]=_DEFAULT_MARK
            ) -> Union[_V, _T]:
        key = self._alter_key(key)

        try:
            with self._lock:
                index = self._pair_ids[key].pop()

                if len(self._pair_ids[key]) == 0:
                    del self._first_values[key]

                    del self._pair_ids[key]

                    del self._last_values[key]

                else:
                    new_last_index = self._pair_ids[key][-1]
                    self._last_values[key] = self._kv_pairs[new_last_index][1]

                _, value = self._kv_pairs.pop(index)

                return value

        except KeyError as e:
            if default is _DEFAULT_MARK:
                raise KeyError(key) from e

            else:
                return default  # type: ignore

    def popitem(self, last: bool=True) -> Tuple[_K, _V]:
        """
        This method behaves exactly like `collections.OrderedDict.popitem`.

        If `last` is `True` then the items will popped by LIFO, else FIFO.
        """
        with self._lock:
            index, pair = self._kv_pairs.popitem(last)

            key, _ = pair

            if len(self._pair_ids[key]) == 1:
                del self._first_values[key]

                del self._pair_ids[key]

                del self._last_values[key]

            elif self._pair_ids[key][-1] == index:
                next_last_index = self._pair_ids[key][-2]

                self._last_values[key] = self._kv_pairs[next_last_index][1]

                self._pair_ids[key].remove(index)

            return pair

    def update(self, *args: Any, **kwargs: Any) -> None:  # Type Hints???
        if args:
            if len(args) > 1:  # pragma: no cover
                raise TypeError(
                    ("update expected at most 1 positional argument, "
                     "got {} args.").format(len(args)))

            elif isinstance(args[0], collections.abc.Mapping):
                    for k, v in args[0].items():
                        self.add(k, v)

            elif isinstance(args[0], collections.abc.Iterable):
                for k, v in args[0]:
                    self.add(k, v)

            else:  # pragma: no cover
                raise TypeError(
                    ("update expected a Mapping or an Iterable "
                     "as the positional argument, got {}.")
                    .format(type(args[0])))

        for k, v in kwargs.items():
            self.add(k, v)

    def clear(self) -> None:
        with self._lock:
            self._first_values.clear()

            self._kv_pairs.clear()
            self._pair_ids.clear()

            self._last_values.clear()

    def setdefault(self, key: _K, default: _V=None) -> _V:
        try:
            return self[key]

        except KeyError:
            self[key] = default  # type: ignore
            return default  # type: ignore
