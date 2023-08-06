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

from magicdict import FrozenTolerantMagicDict


class FrozenTolerantMagicDictTestCase:
    def test_init_with_iter(self):
        sample = [("A", "b"), ("c", "d"), ("c", "d"), ("e", "f")]
        dic = FrozenTolerantMagicDict(sample)

        assert list(dic.items()) == [(k.lower(), v) for k, v in sample]

    def test_init_with_mapping(self):
        sample = {"A": "b", "c": "d", "e": "f"}
        dic = FrozenTolerantMagicDict(sample)

        assert list(dic.items()) == \
            list({"a": "b", "c": "d", "e": "f"}.items())

    def test_init_with_kwargs(self):
        sample = {"a": "b", "c": "d", "e": "f"}
        dic = FrozenTolerantMagicDict(**sample)

        assert sample.items() == dic.items()

    def test_method_getitem(self):
        dic = FrozenTolerantMagicDict([("a", "b"), ("a", "c")])

        assert dic["A"] == "b"

    def test_get_first(self):
        dic = FrozenTolerantMagicDict([("a", "b"), ("A", "d"), ("A", "f")])

        assert dic.get_first("A") == "b"

        assert dic.get_first("b") is None

    def test_get_last(self):
        dic = FrozenTolerantMagicDict([("A", "b"), ("a", "d"), ("a", "f")])

        assert dic.get_last("A") == "f"

        assert dic.get_last("b") is None

    def test_get_iter(self):
        dic = FrozenTolerantMagicDict([("a", "b"), ("A", "d"), ("a", "f")])

        assert list(dic.get_iter("A")) == ["b", "d", "f"]

    def test_copy(self):
        dic = FrozenTolerantMagicDict([("a", "b"), ("a", "d"), ("a", "f")])

        dic_copy = dic.copy()

        assert dic == dic_copy
