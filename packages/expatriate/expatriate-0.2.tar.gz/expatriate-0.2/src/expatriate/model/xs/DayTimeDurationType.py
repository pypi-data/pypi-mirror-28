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
from .DurationType import DurationType

logger = logging.getLogger(__name__)

class DayTimeDurationType(DurationType):
    def parse_value(self, value):
        m = re.fullmatch(r'-?P(\d+D)?(T(\d+H)?(\d+M)?(\d+(\.\d+)?S)?)?', value)
        if not m or not re.fullmatch(r'.*[DHMS].*', value) or not re.fullmatch(r'.*[^T]', value):
            raise ValueError('Unable to parse xs:DayTimeDurationType value')

        return super().parse_value(value)

    def produce_value(self, value):
        months, seconds = value
        if months != 0:
            raise ValueError('xs:DayTimeDurationType requires 0 for months value')

        return super().produce_value(value)
