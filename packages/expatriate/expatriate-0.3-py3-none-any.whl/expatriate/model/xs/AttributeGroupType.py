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
from .AnnotatedType import AnnotatedType
from .AttributeType import AttributeType
from .NCNameType import NCNameType
from .QNameType import QNameType
from .WildcardType import WildcardType

logger = logging.getLogger(__name__)

@attribute(local_name='name', type=NCNameType)
@attribute(local_name='ref', type=QNameType)
@attribute(local_name='*')
@element(local_name='attribute', list='tags',
    cls=('expatriate.model.xs.AttributeType', 'AttributeType'), min=0, max=None)
@element(local_name='attributeGroup', list='tags',
    cls=('expatriate.model.xs.AttributeGroupType', 'AttributeGroupType'),
    min=0, max=None)
@element(local_name='anyAttribute', list='tags', cls=WildcardType, min=0)
class AttributeGroupType(AnnotatedType):
    pass
