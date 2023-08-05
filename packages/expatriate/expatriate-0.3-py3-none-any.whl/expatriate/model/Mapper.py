# Copyright 2016 Casey Jaymes

# This file is part of Expatriate.
#
# Expatriate is free software: you can redistribute it and/or modify
# it under the terms of the GNU Lesser General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# Expatriate is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU Lesser General Public License for more details.
#
# You should have received a copy of the GNU Lesser General Public License
# along with Expatriate.  If not, see <http://www.gnu.org/licenses/>.

import importlib
import logging

logger = logging.getLogger(__name__)

class Mapper(object):
    '''
    Super class of Mapper types. Defines the methods to be overriden and a few
    convenience methods.
    '''
    def __init__(self, **kwargs):
        self._kwargs = kwargs

    def __str__(self):
        return self.__class__.__name__ + ' ' + str(self._kwargs)

    def _load_cls(self, cls_):
        '''
        Wrapper function to either return cls_ if it is a class or load the
        class if it is a tuple of the form (package, class_name)
        '''
        if isinstance(cls_, tuple):
            mod = importlib.import_module(cls_[0])
            return getattr(mod, cls_[1])
        else:
            return cls_

    def initialize(self, *args, **kwargs):
        raise NotImplementedError

    def matches(self, *args, **kwargs):
        raise NotImplementedError

    def parse_in(self, *args, **kwargs):
        raise NotImplementedError

    def validate(self, *args, **kwargs):
        raise NotImplementedError

    def produce_in(self, *args, **kwargs):
        raise NotImplementedError
