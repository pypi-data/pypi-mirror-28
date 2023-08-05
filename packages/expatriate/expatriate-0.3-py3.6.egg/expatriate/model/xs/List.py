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
import re

from ..decorators import *
from .StringType import StringType

logger = logging.getLogger(__name__)

class List(StringType):
    # abstract
    def parse_value(self, value):
        value = super().parse_value(value)

        if len(value) < 1:
            raise ValueError('xs:List must contain at least 1 character')

        r = []
        for i in re.split(r'\s+', value):
            r.append(self.parse_item(i))

        return tuple(r)

    def produce_value(self, value):
        r = []
        for i in value:
            r.append(self.produce_item(i))
        return ' '.join(r)

    def parse_item(self, item_value):
        import inspect
        raise NotImplementedError(inspect.stack()[0][3] + '() has not been implemented in subclass: ' + self.__class__.__name__)

    def produce_item(self, item_value):
        import inspect
        raise NotImplementedError(inspect.stack()[0][3] + '() has not been implemented in subclass: ' + self.__class__.__name__)
