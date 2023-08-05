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
from .QNameType import QNameType

logger = logging.getLogger(__name__)

@attribute(local_name='memberTypes', type=QNameType)
@element(local_name='simpleType', list='tags',
    cls=('expatriate.model.xs.SimpleTypeType', 'SimpleTypeType'),
    min=0, max=None)
class UnionElement(AnnotatedType):
    pass
