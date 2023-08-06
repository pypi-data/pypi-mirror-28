# Copyright 2016 Casey Jaymes

# This file is part of PublishSubscribe.
#
# PublishSubscribe is free software: you can redistribute it and/or modify
# it under the terms of the GNU Lesser General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# PublishSubscribe is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU Lesser General Public License for more details.
#
# You should have received a copy of the GNU Lesser General Public License
# along with PublishSubscribe.  If not, see <http://www.gnu.org/licenses/>.

import logging

from .exceptions import *
from .Publisher import Publisher

logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)

class PublishingList(list, Publisher):
    def __init__(self, *args, **kwargs):
        list.__init__(self, *args, **kwargs)
        Publisher.__init__(self)

    def _slice_to_range(self, slc):
        if slc.step is None:
            return range(slc.start, slc.stop)
        else:
            return range(slc.start, slc.stop, slc.step)

    def __setitem__(self, idx, value):
        if isinstance(idx, int):
            if idx < len(self):
                old = self[idx]
                r = list.__setitem__(self, idx, value)
                self._publish_updated(idx, old, value)
            else:
                r = list.__setitem__(self, idx, value)
                self._publish_added(idx, value)
        elif isinstance(idx, slice):
            adds = []
            updates = []
            for i, v in enumerate(self[idx]):
                if i + idx.start < len(self):
                    updates.append((i + idx.start, v, value[i]))
                else:
                    adds.append((i + idx.start, value[i]))
            r = list.__setitem__(self, idx, value)
            for i, v in adds:
                self._publish_added(i, v)
            for i, old, new in updates:
                self._publish_updated(i, old, new)
        return r

    def __delitem__(self, idx):
        if isinstance(idx, int):
            old = self[idx]
            r = list.__delitem__(self, idx)
            self._publish_deleted(idx, old)
        elif isinstance(idx, slice):
            dels = []
            for i in self._slice_to_range(idx):
                dels.append((i, self[i]))
            r = list.__delitem__(self, idx)
            for i, v in dels:
                self._publish_deleted(i, v)
        return r

    def pop(self, *args):
        if len(args) > 0:
            # assume args[0] is valid or will raise
            idx = args[0]
        else:
            idx = len(self) -1
        old = self[idx]
        r = list.pop(self, *args)
        self._publish_deleted(idx, old)
        return r

    def clear(self):
        old = self.copy()
        r = list.clear(self)
        for i, v in enumerate(old):
            self._publish_deleted(i, v)
        return r

    def append(self, *args):
        r = list.append(self, *args)
        self._publish_added(len(self) - 1, args[0])
        return r

    def extend(self, *args):
        old_len = len(self)
        r = list.extend(self, *args)
        for i, v in enumerate(self[old_len:len(self)]):
            self._publish_added(old_len + i, v)
        return r

    def insert(self, idx, x):
        r = list.insert(self, idx, x)
        self._publish_added(idx)
        for i, v in enumerate(self[idx:len(self)]):
            self._publish_updated(i, v)
        return r

    def remove(self, x):
        old = self.copy()
        for i, v in enumerate(self):
            if v == x:
                idx = i
                break
        # if x doesn't exist; following will throw
        r = list.remove(self, x)
        self._publish_deleted(idx, x)
        for i, v in enumerate(self[idx:len(self)]):
            self._publish_updated(idx + i, old[idx + i], v)
        return r

    def reverse(self):
        r = list.reverse(self)
        for i, v in enumerate(self):
            self._publish_updated(i, v)
        return r
