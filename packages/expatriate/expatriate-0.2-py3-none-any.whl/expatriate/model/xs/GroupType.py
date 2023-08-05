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
from .AnnotatedType import AnnotatedType
from .AnyElement import AnyElement
from .NCNameType import NCNameType
from .NonNegativeIntegerType import NonNegativeIntegerType
from .QNameType import QNameType

logger = logging.getLogger(__name__)

@attribute(local_name='name', type=NCNameType)
@attribute(local_name='ref', type=QNameType)
@attribute(local_name='minOccurs', type=NonNegativeIntegerType, default=1)
@attribute(local_name='maxOccurs', type=AllNniType, default=1)
@attribute(local_name='*', )
@element(local_name='any', list='tags', cls=AnyElement, min=0, max=None)
@element(local_name='element', list='tags',
    cls=('expatriate.model.xs.ElementType', 'ElementType'),
        min=0, max=None)
@element(local_name='group', list='tags',
    cls=('expatriate.model.xs.GroupType', 'GroupType'),
    min=0, max=None)
@element(local_name='all', list='tags',
    cls=('expatriate.model.xs.AllType', 'AllType'),
    min=0, max=None)
@element(local_name='choice', list='tags',
    cls=('expatriate.model.xs.ChoiceElement', 'ChoiceElement'),
    min=0, max=None)
@element(local_name='sequence', list='tags',
    cls=('expatriate.model.xs.GroupType', 'GroupType'),
    min=0, max=None)
class GroupType(AnnotatedType):
    pass
