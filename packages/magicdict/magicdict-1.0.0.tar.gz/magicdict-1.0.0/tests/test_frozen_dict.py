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

from magicdict import FrozenMagicDict


class FrozenMagicDictTestCase:
    def test_init_with_iter(self):
        sample = [("a", "b"), ("c", "d"), ("c", "d"), ("e", "f")]
        dic = FrozenMagicDict(sample)

        assert sample == [(k, v) for k, v in dic.items()]

    def test_init_with_mapping(self):
        sample = {"a": "b", "c": "d", "e": "f"}
        dic = FrozenMagicDict(sample)

        assert sample.items() == dic.items()

    def test_init_with_kwargs(self):
        sample = {"a": "b", "c": "d", "e": "f"}
        dic = FrozenMagicDict(**sample)

        assert sample.items() == dic.items()

    def test_method_getitem(self):
        dic = FrozenMagicDict([("a", "b"), ("a", "c")])

        assert dic["a"] == "b"

    def test_method_iter(self):
        sample = [("a", "b"), ("c", "d"), ("c", "d"), ("e", "f")]
        dic = FrozenMagicDict(sample)

        list(iter(dic)) == ["a", "c", "c", "e"]

    def test_method_len(self):
        sample = [("a", "b"), ("c", "d"), ("c", "d"), ("e", "f")]
        dic = FrozenMagicDict(sample)

        assert len(dic) == 4

    def test_method_contains(self):
        sample = [("a", "b"), ("c", "d"), ("c", "d"), ("e", "f")]
        dic = FrozenMagicDict(sample)

        assert "a" in dic
        assert "d" not in dic

    def test_method_eq_ne(self):
        sample_dic = FrozenMagicDict(
            [("a", "b"), ("c", "d"), ("c", "d"), ("e", "f")])
        dic = FrozenMagicDict(sample_dic)

        assert dic == sample_dic

        sample_ne = dict(sample_dic, f="g")

        assert dic != sample_ne
        assert dic != 123

    def test_method_str(self):
        dic = FrozenMagicDict([("a", "b")])

        assert str(dic) == "FrozenMagicDict([('a', 'b')])"

    def test_method_reversed(self):
        sample = FrozenMagicDict(
            [("a", "b"), ("c", "d"), ("c", "d"), ("e", "f")])
        dic = FrozenMagicDict(sample)

        assert list(reversed(dic)) == list(reversed(sample))

    def test_get_first(self):
        dic = FrozenMagicDict([("a", "b"), ("a", "d"), ("a", "f")])

        assert dic.get_first("a") == "b"

        assert dic.get_first("b") is None

    def test_get_last(self):
        dic = FrozenMagicDict([("a", "b"), ("a", "d"), ("a", "f")])

        assert dic.get_last("a") == "f"

        assert dic.get_last("b") is None

    def test_get_iter(self):
        dic = FrozenMagicDict([("a", "b"), ("a", "d"), ("a", "f")])

        assert list(dic.get_iter("a")) == ["b", "d", "f"]

    def test_get_list(self):
        dic = FrozenMagicDict([("a", "b"), ("a", "d"), ("a", "f")])

        assert dic.get_list("a") == ["b", "d", "f"]

    def test_copy(self):
        dic = FrozenMagicDict([("a", "b"), ("a", "d"), ("a", "f")])

        dic_copy = dic.copy()

        assert dic == dic_copy
