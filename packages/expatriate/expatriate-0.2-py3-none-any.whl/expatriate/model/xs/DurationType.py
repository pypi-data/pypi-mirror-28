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

class DurationType(AnySimpleType):
    def parse_value(self, value):
        m = re.fullmatch(r'-?P(\d+Y)?(\d+M)?(\d+D)?(T(\d+H)?(\d+M)?(\d+(\.\d+)?S)?)?', value)
        if not m or not re.fullmatch(r'.*[YMDHS].*', value) or not re.fullmatch(r'.*[^T]', value):
            raise ValueError('Unable to parse xs:Duration value')

        if value.startswith('-'):
            signed = True
        else:
            signed = False

        # fudge for python 3.5 compatibility w/match obj __getitem__
        m = list(m.groups())
        m.insert(0, None)

        if m[1] is not None:
            years = int(m[1].strip('Y'))
        else:
            years = 0

        if m[2] is not None:
            months = int(m[2].strip('M'))
        else:
            months = 0

        if m[3] is not None:
            days = int(m[3].strip('D'))
        else:
            days = 0

        if m[5] is not None:
            hours = int(m[5].strip('H'))
        else:
            hours = 0

        if m[6] is not None:
            minutes = int(m[6].strip('M'))
        else:
            minutes = 0

        if m[7] is not None:
            seconds = float(m[7].strip('S'))
        else:
            seconds = 0.0

        # collapse years into months
        months += years * 12

        # collapse the rest into seconds
        hours += days * 24
        minutes += hours * 60
        seconds += minutes * 60.0

        if signed:
            return (- months, - seconds)
        else:
            return (months, seconds)

    def produce_value(self, value):
        if not isinstance(value, tuple):
            raise ValueError('xs:duration is produced from a months, seconds tuple')

        months, seconds = value

        if months < 0 or seconds < 0:
            r = '-P'
            months = - months
            seconds = - seconds
        else:
            r = 'P'

        years, months = divmod(months, 12)
        minutes, seconds = divmod(seconds, 60)
        hours, minutes = divmod(int(minutes), 60)
        days, hours = divmod(hours, 24)

        if years != 0:
            r += '%dY' % years
        if months != 0:
            r += '%dM' % months
        if days != 0:
            r += '%dD' % days
        if hours != 0 or minutes != 0 or seconds != 0.0:
            r += 'T'
            if hours != 0:
                r += '%dH' % hours
            if minutes != 0:
                r += '%dM' % minutes
            if seconds != 0.0:
                # be nice if we could print based on float's precision,
                # but we just cut off if it's an int value
                seconds_float = seconds - int(seconds)
                if seconds_float != 0.0:
                    r += '%fS' % seconds
                else:
                    r += '%dS' % int(seconds)

        return r
