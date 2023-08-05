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

import logging

from .exceptions import *
from .Node import Node

logger = logging.getLogger(__name__)

class Parent(Node):
    '''
    Super class for nodes containing children

    :keyword parent: parent Node of this Node
    :type parent: Parent or None

    '''
    def __init__(self, parent=None):
        super().__init__(parent=parent)
        self.children = []

    def spawn_character_data(self, *args, **kwargs):
        '''
        Spawn a :py:class:`.CharacterData` object using this node as the parent

        All arguments are passed to the newly created object's constructor
        '''
        from .CharacterData import CharacterData
        n = CharacterData(*args, **kwargs, parent=self)

        self.children.append(n)

        return n

    def spawn_comment(self, *args, **kwargs):
        '''
        Spawn a :py:class:`.Comment` object using this node as the parent

        All arguments are passed to the newly created object's constructor
        '''
        from .Comment import Comment
        n = Comment(*args, **kwargs, parent=self)

        self.children.append(n)

        return n

    def spawn_element(self, *args, **kwargs):
        '''
        Spawn a :py:class:`.Element` object using this node as the parent

        All arguments are passed to the newly created object's constructor
        '''
        from .Element import Element
        n = Element(*args, **kwargs, parent=self)

        self.children.append(n)

        return n

    def spawn_processing_instruction(self, *args, **kwargs):
        '''
        Spawn a :py:class:`.ProcessingInstruction` object using this node as the parent

        All arguments are passed to the newly created object's constructor
        '''
        from .ProcessingInstruction import ProcessingInstruction
        n = ProcessingInstruction(*args, **kwargs, parent=self)

        self.children.append(n)

        return n

    def __len__(self):
        return len(self.children)

    def __getitem__(self, key):
        if not isinstance(key, int) and not isinstance(key, slice):
            raise TypeError('Key values must be of int type or slice; got: ' + key.__class__.__name__)

        return self.children[key]

    def __setitem__(self, key, value):
        if not isinstance(key, int):
            raise TypeError('Key values must be of int type; got: ' + key.__class__.__name__)
        if not isinstance(value, Node):
            raise TypeError('Values must be of Node type; got: ' + value.__class__.__name__)

        self.children[key] = value

    def __delitem__(self, key):
        if not isinstance(key, int):
            raise TypeError('Key values must be of int type; got: ' + key.__class__.__name__)

        del self.children[key]

    def __iter__(self):
        return iter(self.children)

    def append(self, x):
        from .CharacterData import CharacterData

        if isinstance(x, str):
            # wrap in CharaterData
            n = CharacterData(x, parent=self)
        elif isinstance(x, int) or isinstance(x, float):
            # convert to str & wrap in CharaterData
            n = CharacterData(str(x), parent=self)
        elif isinstance(x, Node):
            n = x
            n._parent = self
        else:
            raise ValueError('Children of ' + self.__class__.__name__
                + ' must be a simple type (str, int, float)'
                + ' or a subclass of Node; got: ' + x.__class__.__name__)

        self.children.append(n)

    def count(self):
        return self.children.count()

    def index(self, x):
        return self.children.index(x)

    def extend(self, iterable):
        for c in iterable:
            self.append(c)

    def insert(self, i, x):
        from .CharacterData import CharacterData

        if isinstance(x, str):
            # wrap in CharaterData
            n = CharacterData(x, parent=self)
        elif isinstance(x, int) or isinstance(x, float):
            # convert to str & wrap in CharaterData
            n = CharacterData(str(x), parent=self)
        elif isinstance(x, Node):
            n = x
        else:
            raise ValueError('Children of ' + self.__class__.__name__ + ' must be subclass of Node; got: ' + x.__class__.__name__)

        self.children.insert(i, n)

    def pop(self, i=-1):
        n = self.children.pop(i)
        self.detach(n)
        return n

    def remove(self, x):
        n = self.children[self.children.index(x)]
        self.children.remove(x)

    def reverse(self):
        return self.children.reverse()

    def sort(self, key=None, reverse=False):
        return self.children.sort(key=key, reverse=reverse)

    # TODO copy()

    def find_by_id(self, id_):
        logger.debug(str(self) + ' checking children for id: ' + str(id_))
        for c in self.children:
            el = c.find_by_id(id_)
            if el is not None:
                return el

        return super().find_by_id(id_)
