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

class ProcessingInstruction(Node):
    '''
    Class representing a XML processing instruction

    :param str target: Target of the PI
    :param str data: Data section of the PI
    :param parent: Parent node of the PI
    :type parent: expatriate.Parent or None
    '''
    def __init__(self, target, data, parent=None):
        super().__init__(parent=parent)

        self.target = target
        self.data = data

    def produce(self):
        '''
        Produce an XML str (not encoded) from the contents of this
        node

        :rtype: str
        '''
        return '<?' + self.target + ' ' + self.data + '?>'

    def get_type(self):
        '''
        Return the type of the node

        :rtype: str
        '''
        return 'processing instruction'

    def get_string_value(self):
        '''
        Return the string value of the node

        :rtype: str
        '''
        return self.data

    def get_expanded_name(self):
        '''
        Return the expanded name of the node

        :rtype: tuple(None, target)
        '''
        return (None, self.target)
