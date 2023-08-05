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

    :param parent: parent Node of this Node
    :type parent: Parent or None

    '''
    def __init__(self, parent=None):
        super().__init__(parent=parent)
        self.children = []

    def spawn_character_data(self, *args, **kwargs):
        '''
        Spawn a :py:class:`.CharacterData` object using this node as the parent

        All arguments are passed to the newly created object's constructor

        :rtype: expatriate.CharacterData
        '''
        from .CharacterData import CharacterData
        n = CharacterData(*args, **kwargs, parent=self)

        self.children.append(n)

        return n

    def spawn_comment(self, *args, **kwargs):
        '''
        Spawn a :py:class:`.Comment` object using this node as the parent

        All arguments are passed to the newly created object's constructor

        :rtype: expatriate.Comment
        '''
        from .Comment import Comment
        n = Comment(*args, **kwargs, parent=self)

        self.children.append(n)

        return n

    def spawn_element(self, *args, **kwargs):
        '''
        Spawn a :py:class:`.Element` object using this node as the parent

        All arguments are passed to the newly created object's constructor

        :rtype: expatriate.Element
        '''
        from .Element import Element
        n = Element(*args, **kwargs, parent=self)

        self.children.append(n)

        return n

    def spawn_processing_instruction(self, *args, **kwargs):
        '''
        Spawn a :py:class:`.ProcessingInstruction` object using this node as the parent

        All arguments are passed to the newly created object's constructor

        :rtype: expatriate.ProcessingInstruction
        '''
        from .ProcessingInstruction import ProcessingInstruction
        n = ProcessingInstruction(*args, **kwargs, parent=self)

        self.children.append(n)

        return n

    def __len__(self):
        '''
        Returns the length of this node's children.
        '''
        return len(self.children)

    def __getitem__(self, key):
        '''
        Returns the indexed child from the node's children
        '''
        if not isinstance(key, int) and not isinstance(key, slice):
            raise TypeError('Key values must be of int type or slice; got: ' + key.__class__.__name__)

        return self.children[key]

    def __setitem__(self, key, value):
        '''
        Sets the indexed child in the node's children
        '''
        if not isinstance(key, int):
            raise TypeError('Key values must be of int type; got: ' + key.__class__.__name__)
        if not isinstance(value, Node):
            raise TypeError('Values must be of Node type; got: ' + value.__class__.__name__)

        self.children[key] = value

    def __delitem__(self, key):
        '''
        Deletes the indexed child in the node's children
        '''
        if not isinstance(key, int):
            raise TypeError('Key values must be of int type; got: ' + key.__class__.__name__)

        del self.children[key]

    def __iter__(self):
        '''
        Returns an iter on the node's children
        '''
        return iter(self.children)

    def append(self, x):
        '''
        Add an item to the end of the node's children

        :param x: The item to add
        :type x: str or int or float or bool or expatriate.Node
        '''
        from .CharacterData import CharacterData

        if isinstance(x, str):
            # wrap in CharaterData
            n = CharacterData(x, parent=self)
        elif (
            isinstance(x, int)
            or isinstance(x, float)
            or isinstance(x, bool)
        ):
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

    def count(self, x):
        '''
        Returns the number of times node x appears in the node's children

        :param expatriate.Node x: The node
        '''
        return self.children.count(x)

    def index(self, x, *args):
        '''
        Returns zero-based index in the node's children of the first item
        which is x.

        :param expatriate.Node x: The node
        :param int start: Interpreted as the start in slice notation. Optional
        :param int end: Interpreted as the end in slice notation. Optional
        :rtype: int
        :raises ValueError: if there is no such item
        '''
        return self.children.index(x, *args)

    def extend(self, iterable):
        '''
        Extend the node's children by appending all the items from the
        iterable.

        :param list[expatriate.Node] iterable: The iterable which returns items appropriate for appending to the node's children
        '''
        for c in iterable:
            self.append(c)

    def insert(self, i, x):
        '''
        Insert an item at a given position in the node's children.

        :param int i: The index of the item before which to insert.
        :param expatriate.Node x: The node to insert.
        '''
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

    def pop(self, *args):
        '''
        Remove the item at the given position in the node's children, and
        return it. If no index is specified, pop() removes and returns the last
        item in the children.

        :param int i: The position to remove. Optional.
        :rtype: expatriate.Node
        '''
        n = self.children.pop(*args)
        self.detach(n)
        return n

    def remove(self, x):
        '''
        Remove the first item from the node's children whose value is x. It is
        an error if there is no such item.

        :param expatriate.Node x: The node to remove.
        '''
        n = self.children[self.children.index(x)]
        self.children.remove(x)

    def reverse(self):
        '''
        Reverse the items of the node's children in place.
        '''
        self.children.reverse()

    def sort(self, key=None, reverse=False):
        '''
        Sort the items of the list in place.

        :param key: Specifies a function of one argument that is used to extract a comparison key from each list element: key=str.lower. Defaults to None (compare the elements directly).
        :type key: function or None
        :param bool reverse: A boolean value. If set to True, then the list elements are sorted as if each comparison were reversed. Defaults to False.
        '''
        self.children.sort(key=key, reverse=reverse)

    # TODO copy()

    def find_by_id(self, ref):
        '''
        Find the node referenced by *ref* within this node's children.

        :param str ref: The id attribute of the node to match
        :rtype: Node or None
        '''
        logger.debug(str(self) + ' checking children for id: ' + str(ref))
        for c in self.children:
            el = c.find_by_id(ref)
            if el is not None:
                return el

        return super().find_by_id(ref)
