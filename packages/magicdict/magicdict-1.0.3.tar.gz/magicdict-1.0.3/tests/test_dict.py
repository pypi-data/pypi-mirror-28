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

from magicdict import MagicDict

import pytest


class MagicDictTestCase:
    def test_method_init(self):
        sample = [("a", "b"), ("c", "d"), ("c", "d"), ("e", "f")]
        dic = MagicDict(sample)

        assert sample == [(k, v) for k, v in dic.items()]

    def test_method_getitem(self):
        dic = MagicDict([("a", "b"), ("a", "c")])

        assert dic["a"] == "b"

    def test_method_setitem(self):
        dic = MagicDict([("a", "b"), ("a", "c")])

        dic["a"] = "d"

        assert dic["a"] == "d"
        assert dic == {"a": "d"}

    def test_method_delitem(self):
        dic = MagicDict([("a", "b"), ("a", "c")])

        del dic["a"]

        with pytest.raises(KeyError):
            dic["a"]

    def test_get_last(self):
        dic = MagicDict([("a", "b"), ("a", "d"), ("a", "f")])

        assert dic.get_last("a") == "f"

        assert dic.get_last("b") is None

    def test_get_iter(self):
        dic = MagicDict([("a", "b"), ("a", "d"), ("a", "f")])

        assert list(dic.get_iter("a")) == ["b", "d", "f"]

    def test_add(self):
        dic = MagicDict()
        assert dic.get_list("a") == []

        dic.add("a", "b")
        assert dic.get_list("a") == ["b"]

        dic.add("a", "c")
        assert dic.get_list("a") == ["b", "c"]

    def test_pop(self):
        dic = MagicDict([("a", "b"), ("a", "c")])

        assert len(dic) == 2

        with pytest.raises(KeyError):
            dic.pop("d")
        assert dic.pop("d", "e") == "e"

        assert dic.pop("a", "e") == "c"

        assert dic.pop("a", "e") == "b"
        assert len(dic) == 0

    def test_popitem(self):
        dic = MagicDict([("a", "b"), ("a", "c")])

        assert dic.popitem() == ("a", "c")
        assert dic.popitem() == ("a", "b")

        with pytest.raises(KeyError):
            dic.popitem()

        dic = MagicDict([("a", "b"), ("a", "c")])

        assert dic.popitem(False) == ("a", "b")

    def test_update(self):
        dic = MagicDict()

        dic.update({"a": "b"})
        assert dic.get_list("a") == ["b"]

        dic.update([("a", "c")], a="d")
        assert dic.get_list("a") == ["b", "c", "d"]

    def test_clear(self):
        dic = MagicDict([("a", "b"), ("a", "d"), ("a", "f")])

        assert len(dic) == 3

        dic.clear()

        assert len(dic) == 0

    def test_setdefault(self):
        dic = MagicDict([("a", "b")])

        dic.setdefault("a", "c")
        dic.setdefault("e", "f")

        assert dic["a"] == "b"
        assert dic["e"] == "f"

    def test_fromkeys(self):
        dic = MagicDict.fromkeys(["a", "b", "b"], "d")

        assert dic.get_list("a") == ["d"]
        assert dic.get_list("b") == ["d", "d"]

    def test_copy(self):
        dic = MagicDict([("a", "b"), ("a", "d"), ("a", "f")])

        dic_copy = dic.copy()

        assert dic == dic_copy
