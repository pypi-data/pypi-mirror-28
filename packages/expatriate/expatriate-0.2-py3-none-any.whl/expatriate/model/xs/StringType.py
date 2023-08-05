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
from .AnySimpleType import AnySimpleType

logger = logging.getLogger(__name__)

class StringType(AnySimpleType):
    def get_value_pattern(self):
        return None

    def get_value_enum(self):
        return None

    def parse_value(self, value):
        if not isinstance(value, str):
            raise TypeError('xs:string requires a str value for initialization, got ' + value.__class__.__name__)

        p = self.get_value_pattern()
        if p is not None and not re.fullmatch(p, value):
            raise ValueError(self.__class__.__name__ + ' requires a value matching ' + p)

        e = self.get_value_enum()
        if e is not None and value not in e:
            raise ValueError(self.__class__.__name__ + ' requires a value in ' + str(e))

        return value
