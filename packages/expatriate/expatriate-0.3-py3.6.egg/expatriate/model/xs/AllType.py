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
from .AnnotationElement import AnnotationElement
from .ElementType import ElementType
from .GroupType import GroupType

logger = logging.getLogger(__name__)

@attribute(local_name='minOccurs', enum=['0', '1'], default='1')
@attribute(local_name='maxOccurs', enum=['1'], default='1')
@attribute(local_name='*')
@element(local_name='annotation', list='tags', cls=AnnotationElement, min=0)
@element(local_name='element', list='tags', cls=ElementType, min=0, max=None)
class AllType(GroupType):
    pass
