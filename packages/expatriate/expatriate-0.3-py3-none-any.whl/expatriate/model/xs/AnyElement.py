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

from ..decorators import *
from .AllNniType import AllNniType
from .NonNegativeIntegerType import NonNegativeIntegerType
from .WildcardType import WildcardType

logger = logging.getLogger(__name__)

@attribute(local_name='minOccurs', type=NonNegativeIntegerType, default=1)
@attribute(local_name='maxOccurs', type=AllNniType, default=1)
class AnyElement(WildcardType):
    def get_defs(self, schema):
        model_map = {'elements': [], 'attributes': {}}

        tag = {'tag_name': '*', 'min': 0}
        if self.namespace != '##any':
            tag['namespace'] = self.namespace
        model_map['elements'].append(tag)

        return model_map
