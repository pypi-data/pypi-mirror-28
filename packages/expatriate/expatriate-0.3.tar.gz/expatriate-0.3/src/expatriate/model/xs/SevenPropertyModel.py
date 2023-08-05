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

import datetime as dt  # avoids conflict with init kwarg
import logging
import re

from ..decorators import *

logger = logging.getLogger(__name__)

class SevenPropertyModel(object):
    def __init__(
        self,
        datetime=None,
        time=None,
        date=None,
        year=None,
        month=None,
        day=None,
        hour=None,
        minute=None,
        second=None,
        timezoneOffset=None
    ):

        self._year = None
        self._month = None
        self._day = None
        self._hour = None
        self._minute = None
        self._second = None
        self._timezoneOffset = None

        if datetime is not None:
            year = datetime.year
            month = datetime.month
            day = datetime.day
            hour = datetime.hour
            minute = datetime.minute
            second = datetime.second
            if datetime.tzinfo is not None:
                try:
                    timezoneOffset = datetime.tzinfo.utcoffset(datetime)
                    if isinstance(timezoneOffset, dt.timedelta):
                        if timezoneOffset.days > 0:
                            day += timezoneOffset.days
                        timezoneOffset = timezoneOffset.seconds / 60
                except:
                    pass

        if time is not None:
            hour = time.hour
            minute = time.minute
            second = time.second
            if time.tzinfo is not None:
                try:
                    timezoneOffset = time.tzinfo.utcoffset(time)
                    if isinstance(timezoneOffset, dt.timedelta):
                        if timezoneOffset.days > 0:
                            day += timezoneOffset.days
                        timezoneOffset = timezoneOffset.seconds / 60
                except:
                    pass

        if date is not None:
            year = date.year
            month = date.month
            day = date.day

        if year is not None:
            self.year = year

        if month is not None:
            self.month = month

        if day is not None:
            self.day = day

        if hour is not None:
            self.hour = hour

        if minute is not None:
            self.minute = minute

        if second is not None:
            self.second = second

        if timezoneOffset is not None:
            self.timezoneOffset = timezoneOffset

    @property
    def year(self):
        return self._year

    @year.setter
    def year(self, value):
        if isinstance(value, str):
            value = int(value)
        elif not isinstance(value, int):
            raise TypeError('Year must be an int')

        self._year = value

    @property
    def month(self):
        return self._month

    @month.setter
    def month(self, value):
        if isinstance(value, str):
            value = int(value)
        elif not isinstance(value, int):
            raise TypeError('month must be an int')

        if value < 1 or value > 12:
            raise ValueError('month must be between 1 and 12')

        self._month = value

    @property
    def day(self):
        return self._day

    @day.setter
    def day(self, value):
        if isinstance(value, str):
            value = int(value)
        elif not isinstance(value, int):
            raise TypeError('day must be an int')

        if value < 1 or value > 31:
            raise ValueError('day must be between 1 and 31')

        self._day = value

    @property
    def hour(self):
        return self._hour

    @hour.setter
    def hour(self, value):
        if isinstance(value, str):
            value = int(value)
        elif not isinstance(value, int):
            raise TypeError('hour must be an int')

        if value < 0 or value > 23:
            raise ValueError('hour must be between 0 and 23')

        self._hour = value

    @property
    def minute(self):
        return self._minute

    @minute.setter
    def minute(self, value):
        if isinstance(value, str):
            value = int(value)
        elif not isinstance(value, int):
            raise TypeError('minute must be an int')

        if value < 0 or value > 59:
            raise ValueError('minute must be between 0 and 59')

        self._minute = value

    @property
    def second(self):
        return self._second

    @second.setter
    def second(self, value):
        if isinstance(value, str) or isinstance(value, int):
            value = float(value)
        elif not isinstance(value, float):
            raise TypeError('second must be a float')

        if value < 0.0 or value >= 60.0:
            raise ValueError('second must be between 0 and 60')

        self._second = value

    @property
    def timezoneOffset(self):
        return self._timezoneOffset

    @timezoneOffset.setter
    def timezoneOffset(self, value):
        if isinstance(value, str):
            if value == 'Z' or value == '+00:00' or value == '-00:00':
                value = 0
            elif ':' in value:
                tz_hour, tz_minute = value.split(':')
                value = (int(tz_hour) * 60) + int(tz_minute)
            else:
                value = int(timezoneOffset)
        elif not isinstance(value, int):
            raise TypeError('timezoneOffset must be an int')

        if value < -840 or value > 840:
            raise ValueError('timezoneOffset must be between -840 and 840')

        self._timezoneOffset = value

    def _tz_to_string(self):
        if self._timezoneOffset is None:
            return ''
        elif self._timezoneOffset == 0:
            return 'Z'
        else:
            tz_hour, tz_minute = divmod(self._timezoneOffset, 60)
            if self._timezoneOffset > 0:
                return '+%02d:%02d' % (int(tz_hour), tz_minute)
            else:
                return '-%02d:%02d' % (int(tz_hour), tz_minute)

    def __str__(self):
        if (
            self._year is None
            and self._month is None
            and self._day is not None
            and self._hour is None
            and self._minute is None
            and self._second is None
        ):
            # gDay
            return "---%02d%s" % (self._day, self._tz_to_string())

        elif (
            self._year is None
            and self._month is not None
            and self._day is None
            and self._hour is None
            and self._minute is None
            and self._second is None
        ):
            # gMonth
            return "--%02d%s" % (self._month, self._tz_to_string())

        elif (
            self._year is None
            and self._month is not None
            and self._day is not None
            and self._hour is None
            and self._minute is None
            and self._second is None
        ):
            # gMonthDay
            return "--%02d-%02d%s" % (self._month, self._day, self._tz_to_string())

        elif (
            self._year is not None
            and self._month is None
            and self._day is None
            and self._hour is None
            and self._minute is None
            and self._second is None
        ):
            # gYear
            return "%04d%s" % (self._year, self._tz_to_string())

        elif (
            self._year is not None
            and self._month is not None
            and self._day is None
            and self._hour is None
            and self._minute is None
            and self._second is None
        ):
            # gYearMonth
            return "%04d-%02d%s" % (self._year, self._month, self._tz_to_string())

        elif (
            self._year is not None
            and self._month is not None
            and self._day is not None
            and self._hour is None
            and self._minute is None
            and self._second is None
        ):
            # Date
            return "%04d-%02d-%02d%s" % (self._year, self._month, self._day, self._tz_to_string())

        elif (
            self._year is None
            and self._month is None
            and self._day is None
            and self._hour is not None
            and self._minute is not None
            and self._second is not None
        ):
            # Time
            if self._second - int(self._second) == 0.0:
                return "%02d:%02d:%02.0f%s" % (self._hour, self._minute, self._second, self._tz_to_string())
            else:
                return "%02d:%02d:%02.6f%s" % (self._hour, self._minute, self._second, self._tz_to_string())

        elif (
            self._year is not None
            and self._month is not None
            and self._day is not None
            and self._hour is not None
            and self._minute is not None
            and self._second is not None
        ):
            # DateTime
            if self._second - int(self._second) == 0.0:
                return "%04d-%02d-%02dT%02d:%02d:%02.0f%s" % (
                    self._year,
                    self._month,
                    self._day,
                    self._hour,
                    self._minute,
                    self._second,
                    self._tz_to_string()
                )
            else:
                return "%04d-%02d-%02dT%02d:%02d:%02.6f%s" % (
                    self._year,
                    self._month,
                    self._day,
                    self._hour,
                    self._minute,
                    self._second,
                    self._tz_to_string()
                )

        else:
            raise NotImplementedError(
                'Value set '
                + str([
                    self._year,
                    self._month,
                    self._day,
                    self._hour,
                    self._minute,
                    self._second
                ])
                + ' cannot be converted to a string'
            )

    def __eq__(self, other):
        if not isinstance(other, SevenPropertyModel):
            return False

        if self._year != other._year:
            return False

        if self._month != other._month:
            return False

        if self._day != other._day:
            return False

        if self._hour != other._hour:
            return False

        if self._minute != other._minute:
            return False

        if self._second != other._second:
            return False

        if self._timezoneOffset != other._timezoneOffset:
            return False

        return True

    def to_datetime(self):
        ms = int((self._second - int(self._second)) * 1000)

        if self._timezoneOffset is None:
            return dt.datetime(
                year=self._year,
                month=self._month,
                day=self._day,
                hour=self._hour,
                minute=self._minute,
                second=int(self._second),
                microsecond=ms
            )
        else:
            tz = dt.timezone(
                offset=dt.timedelta(
                    minutes=self._timezoneOffset
                )
            )

            return dt.datetime(
                year=self._year,
                month=self._month,
                day=self._day,
                hour=self._hour,
                minute=self._minute,
                second=int(self._second),
                microsecond=ms,
                tzinfo=tz
            )

    def to_date(self):
        # TODO work around date's timezone naiveté
        return dt.date(
            year=self._year,
            month=self._month,
            day=self._day
        )

    def to_time(self):
        ms = int((self._second - int(self._second)) * 1000)

        if self._timezoneOffset is None:
            return dt.time(
                hour=self._hour,
                minute=self._minute,
                second=int(self._second),
                microsecond=ms
            )
        else:
            tz = dt.timezone(
                offset=dt.timedelta(
                    minutes=self._timezoneOffset
                )
            )

            return dt.time(
                hour=self._hour,
                minute=self._minute,
                second=int(self._second),
                microsecond=ms,
                tzinfo=tz
            )
