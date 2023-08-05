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

import datetime
import logging
import re

from ..decorators import *
from .AnySimpleType import AnySimpleType
from .SevenPropertyModel import SevenPropertyModel

logger = logging.getLogger(__name__)

class DateTimeType(AnySimpleType):
    def parse_value(self, value):
        m = re.fullmatch(r'(-?\d\d\d\d)-(\d\d)-(\d\d)T(\d\d):(\d\d):(\d\d(\.\d+)?)((([-+])(\d\d):(\d\d))|Z)?', value)
        if not m:
            raise ValueError('Unable to parse DateTime value')

        # fudge for python 3.5 compatibility w/match obj __getitem__
        m = list(m.groups())
        m.insert(0, None)

        return SevenPropertyModel(year=m[1], month=m[2], day=m[3], hour=m[4], minute=m[5], second=m[6], timezoneOffset=m[8])
