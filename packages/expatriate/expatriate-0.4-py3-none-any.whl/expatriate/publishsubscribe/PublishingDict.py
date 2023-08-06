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

class PublishingDict(dict, Publisher):
    def __init__(self, *args, **kwargs):
        dict.__init__(self, *args, **kwargs)
        Publisher.__init__(self)

    def __setitem__(self, key, value):
        if key not in self:
            r = dict.__setitem__(self, key, value)
            self._publish_added(key, value)
        else:
            old = self[key]
            r = dict.__setitem__(self, key, value)
            self._publish_updated(key, old, value)
        return r

    def __delitem__(self, key):
        v = self[key]
        r = dict.__delitem__(self, key)
        self._publish_deleted(key, v)
        return r

    def pop(self, *args):
        if args[0] in self:
            r = dict.pop(self, *args)
            self._publish_deleted(args[0], r)
            return r
        else:
            return dict.pop(self, *args)

    def popitem(self):
        r = dict.popitem(self)
        self._publish_deleted(r[0], r[1])
        return r

    def clear(self):
        old = self.copy()
        r = dict.clear(self)
        for k, v in old.items():
            self._publish_deleted(k, v)
        return r

    def update(self, *args, **kwargs):
        updates = []
        if len(args) > 0 and isinstance(args[0], dict):
            for k,v in args[0].items():
                try:
                    updates.append((k, self[k], v))
                except:
                    updates.append((k, None, v))
        elif len(args) > 0 and hasattr(args[0], '__iter__'):
            for k,v in args[0]:
                try:
                    updates.append((k, self[k], v))
                except:
                    updates.append((k, None, v))
        else:
            for k, v in kwargs.items():
                try:
                    updates.append((k, self[k], v))
                except:
                    updates.append((k, None, v))
        r = dict.update(self, *args, **kwargs)
        for k, old, new in updates:
            self._publish_updated(k, old, new)
        return r

    def setdefault(self, *args):
        if args[0] in self:
            r = dict.setdefault(self, *args)
        else:
            r = dict.setdefault(self, *args)
            if len(args) > 1:
                self._publish_added(args[0], args[1])
            else:
                self._publish_added(args[0], None)
        return r
