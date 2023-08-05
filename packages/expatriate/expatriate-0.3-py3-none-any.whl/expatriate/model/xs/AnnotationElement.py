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
from .AnyTypeType import AnyTypeType
from .AppinfoElement import AppinfoElement
from .DocumentationElement import DocumentationElement
from .IdType import IdType

logger = logging.getLogger(__name__)

@attribute(local_name='id', type=IdType)
@element(local_name='appinfo', list='tags', cls=AppinfoElement, min=0, max=None)
@element(local_name='documentation', list='tags', cls=DocumentationElement, min=0, max=None)
class AnnotationElement(AnyTypeType):
    pass
