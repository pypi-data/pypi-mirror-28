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

from magicdict import TolerantMagicDict

import pytest


class TolerantMagicDictTestCase:
    def test_method_init(self):
        sample = [("a", "b"), ("c", "d"), ("c", "d"), ("e", "f")]
        dic = TolerantMagicDict(sample)

        assert dic.items() == [(k.lower(), v) for k, v in sample]

    def test_method_getitem(self):
        dic = TolerantMagicDict([("a", "b"), ("a", "c")])

        assert dic["A"] == "b"

    def test_method_setitem(self):
        dic = TolerantMagicDict([("a", "b"), ("a", "c")])

        dic["A"] = "d"

        assert dic["a"] == "d"

    def test_method_delitem(self):
        dic = TolerantMagicDict([("a", "b"), ("a", "c")])

        "b" in dic.values()
        "c" in dic.values()

        del dic["A"]

        with pytest.raises(KeyError):
            dic["a"]

        "b" not in dic.values()
        "c" not in dic.values()

    def test_get_last(self):
        dic = TolerantMagicDict([("a", "b"), ("a", "d"), ("a", "f")])

        assert dic.get_last("A") == "f"

        assert dic.get_last("b") is None

    def test_get_iter(self):
        dic = TolerantMagicDict([("a", "b"), ("a", "d"), ("a", "f")])

        assert list(dic.get_iter("A")) == ["b", "d", "f"]

    def test_add(self):
        dic = TolerantMagicDict()
        assert dic.get_list("a") == []

        dic.add("A", "b")
        assert dic.get_list("a") == ["b"]

        dic.add("a", "c")
        assert dic.get_list("a") == ["b", "c"]

    def test_pop(self):
        dic = TolerantMagicDict([("a", "b")])

        assert len(dic) == 1

        with pytest.raises(KeyError):
            dic.pop("d")
        assert dic.pop("d", "e") == "e"

        assert dic.pop("A", "e") == "b"
        assert len(dic) == 0

    def test_copy(self):
        dic = TolerantMagicDict([("A", "b"), ("a", "d"), ("a", "f")])

        dic_copy = dic.copy()

        assert dic == dic_copy
