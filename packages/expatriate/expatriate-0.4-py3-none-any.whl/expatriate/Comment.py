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

from .Node import Node

logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)

class Comment(Node):
    '''
    Class representing a XML comment

    :param str data: The contents of this Comment
    :param parent: The node to use as the parent to this node
    :type parent: expatriate.Parent or None
    '''
    def __init__(self, data, parent=None):
        super().__init__(parent=parent)

        self.data = data

    def produce(self):
        '''
        Produce an XML str (not encoded) from the contents of this
        node

        :rtype: str
        '''
        return '<!--' + self.data + '-->'

    def get_string_value(self):
        '''
        Return the string value of the node

        :rtype: str
        '''
        return self.data

    def get_type(self):
        '''
        Return the type of the node

        :rtype: str
        '''
        return 'comment'
