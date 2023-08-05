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

class CharacterData(Node):
    '''
    Class representing XML character data
    '''
    def __init__(self, data, cdata_block=False, parent=None):
        super().__init__(parent=parent)

        self.data = data
        self.cdata_block = cdata_block

    def produce(self):
        s = ''
        if self.cdata_block:
            s += '<![CDATA[' + self.data.replace(']]>', ']]&gt;') + ']]>'
        else:
            s += self.escape(self.data)
        return s

    def get_string_value(self):
        '''
        Return the string value of the node
        '''
        return self.data

    def get_type(self):
        '''
        Return the type of the node
        '''
        return 'text'

    def __eq__(self, other):
        if isinstance(other, str):
            return self.data == other
        elif isinstance(other, int) or isinstance(other, float):
            return self.data == str(other)
        else:
            return object.__eq__(self, other)
