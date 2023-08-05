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

from . import FORM_CHOICE_ENUMERATION
from ..decorators import *
from .AnnotatedType import AnnotatedType
from .NCNameType import NCNameType
from .QNameType import QNameType
from .SimpleTypeType import SimpleTypeType
from .StringType import StringType

logger = logging.getLogger(__name__)

@attribute(local_name='name', type=NCNameType)
@attribute(local_name='ref', type=QNameType)
@attribute(local_name='type', type=QNameType)
@attribute(local_name='use', enum=['prohibited', 'optional', 'required'], default='optional')
@attribute(local_name='default', type=StringType)
@attribute(local_name='fixed', type=StringType)
@attribute(local_name='form', enum=FORM_CHOICE_ENUMERATION)
@attribute(local_name='*', )
@element(local_name='simpleType', list='tags', cls=SimpleTypeType, min=0)
class AttributeType(AnnotatedType):
    pass
