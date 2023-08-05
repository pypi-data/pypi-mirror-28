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

import expatriate

from ..Node import Node
from .exceptions import *
from .Mapper import Mapper

logger = logging.getLogger(__name__)

class ContentMapper(Mapper):
    '''
        **kwargs**

        enum
            Enumeration the attribute's value must be from
        pattern
            Pattern which the value must match.
        type
            Type against which a value must validate

        min
            The minimum value of the content. Can be numeric or None (the
            default).
        max
            The maximum value of the content. Can be numeric or None (the
            default).
    '''

    def initialize(self, model):
        from .Model import Model
        pass

    def validate(self, model):
        from .Model import Model
        pass

    def produce_in(self, el, model, id_):
        from .Model import Model
        logger.debug(str(self) + ' producing ' + str(id_) + ' in ' + str(el))
        el.children.append(expatriate.CharacterData(str(id_)))
