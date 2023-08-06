magicdict
=========
.. image:: https://codecov.io/gl/futursolo/magicdict/branch/master/graph/badge.svg
  :target: https://codecov.io/gl/futursolo/magicdict

.. image:: https://gitlab.com/futursolo/magicdict/badges/master/build.svg
  :target: https://gitlab.com/futursolo/magicdict/commits/master

An ordered, one-to-many mapping.

Install
-------

.. code-block:: shell

   $ pip install -U magicdict

Thread Safety
-------------
:code:`FrozenMagicDict` and its subclasses should be thread safe without additional
locking. If any data races occurred, then that's a bug. Please file an issue
with reproducing procedure.

Usage
-----
:code:`MagicDict` should function like :code:`collections.OrderedDict` except
:code:`move_to_end` is not defined and :code:`d[key]` always returns the first
item.

:code:`FrozenMagicDict` is an immutable version of :code:`MagicDict`.

:code:`FrozenTolerantMagicDict` and :code:`TolerantMagicDict` are
case-insensitive versions of :code:`FrozenMagicDict` and :code:`MagicDict`
respectively.

:code:`get_first`, :code:`get_last`, :code:`get_iter`, and :code:`get_list`:
These methods are available in `FrozenMagicDict` and its subclasses.
For more details, please read the comments of each method.

:code:`add`:
Method :code:`add` is available in :code:`MagicDict` and
:code:`TolerantMagicDict`. This method is used as an substitution of
:code:`dic[key] = value` as it can append a value to the
dictionary without removing the existing one. Setting values like normal
:code:`OrderedDict` will clear the stored value(s) if any.

Contributing
------------
The repository is hosted on `GitLab <https://gitlab.com/futursolo/magicdict>`_.

License
-------
Copyright 2018 Kaede Hoshikawa

Licensed under the Apache License, Version 2.0 (the "License");
you may not use this file except in compliance with the License.
You may obtain a copy of the License at

    http://www.apache.org/licenses/LICENSE-2.0

Unless required by applicable law or agreed to in writing, software
distributed under the License is distributed on an "AS IS" BASIS,
WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
See the License for the specific language governing permissions and
limitations under the License.
