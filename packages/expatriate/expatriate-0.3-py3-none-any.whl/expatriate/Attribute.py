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
from .xpath.Literal import Literal

logger = logging.getLogger(__name__)

class Attribute(Node):
    '''
    Class representing a XML attribute node

    :param str local_name: Local name of the attribute (the part after the :)
    :param str value: The value of the attribute
    :param parent: The node to use as the parent to this node
    :type parent: expatriate.Parent or None
    :param prefix: The prefix used in this attribute's name (the part before the :)
    :type prefix: str or None
    :param namespace: The namespace of this Attribute. Must be defined if the prefix is not defined by the parent Nodes
    :type namespace: str or None
    '''
    def __init__(self, local_name, value, parent=None, prefix=None, namespace=None):
        super().__init__(parent=parent)

        self._prefix = prefix
        self._local_name = local_name
        self._namespace = namespace

        self.value = value

    @property
    def name(self):
        """
        The name of this Attribute.

        :getter: Returns the name.
        :setter: Sets the name. Updates the prefix and namespace and local_name if they change.
        :type: str
        """
        if self._prefix is None:
            return self._local_name
        else:
            return self._prefix + ':' + self._local_name

    @name.setter
    def name(self, name):
        if ':' in name:
            self._prefix, colon, self._name = name.partition(':')
        else:
            self._prefix = None
            self._name = name

        self._namespace = self.prefix_to_namespace(self._prefix)

    @property
    def local_name(self):
        """
        The local name (part after the :) of this Attribute.

        :getter: Returns the local name.
        :setter: Sets the local name.
        :type: str
        """
        return self._local_name

    @local_name.setter
    def local_name(self, local_name):
        self._local_name = local_name

    @property
    def prefix(self):
        """
        The prefix (part before the :) of this Attribute.

        :getter: Returns the prefix.
        :setter: Sets the prefix.
        :type: str
        """
        return self._prefix

    @prefix.setter
    def prefix(self, prefix):
        self._prefix = prefix
        self._namespace = self.prefix_to_namespace(self._prefix)

    @property
    def namespace(self):
        """
        The namespace (URI the prefix maps to) of this Attribute.

        :getter: Returns the namespace URI.
        :setter: Sets the namespace URI.
        :type: str
        """
        return self._namespace

    @namespace.setter
    def namespace(self, namespace):
        self._namespace = namespace
        self._prefix = self.namespace_to_prefix(namespace)

    def get_type(self):
        '''
        Return the type of the node

        :rtype: str
        '''
        return 'attribute'

    def get_string_value(self):
        '''
        Return the string value of the node

        :rtype: str
        '''
        return self.value

    def get_expanded_name(self):
        '''
        Return the expanded name of the node

        :rtype: tuple(namespace str, local_name str)
        '''
        return (self.namespace, self.local_name)

    def __eq__(self, other):
        if isinstance(other, Literal):
            return self.value == other.value
        elif isinstance(other, str):
            return self.value == other
        elif isinstance(other, int) or isinstance(other, float):
            return self.value == str(other)
        return object.__eq__(self, other)

    def __str__(self):
        s = self.__class__.__name__ + ' ' + hex(id(self)) + ' '
        if self.namespace is not None:
            s += self.namespace + ':'
        s += self.local_name + '=' + self.value
        return s

    def get_document_order(self):
        '''
        Get the index of this Node's order in the enclosing Document.

        :rtype: int
        :raises UnattachedElementException: if the Node is not attached to a Document
        '''
        if self._parent is None:
            raise UnattachedElementException('Attribute ' + str(self) + ' is not attached to a document')

        do = self._parent.get_document_order()
        do += len(self._parent.namespace_nodes)
        ordered_attr = [self._parent.attribute_nodes[k] for k in sorted(self._parent.attribute_nodes.keys())]
        return do + ordered_attr.index(self)
