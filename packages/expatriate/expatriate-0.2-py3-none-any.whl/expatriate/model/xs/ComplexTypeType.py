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
import os.path

from ..decorators import *
from .AnnotatedType import AnnotatedType
from .AttributeGroupType import AttributeGroupType
from .AttributeType import AttributeType
from .BooleanType import BooleanType
from .ChoiceElement import ChoiceElement
from .ComplexContentElement import ComplexContentElement
from .GroupType import GroupType
from .NCNameType import NCNameType
from .SimpleContentElement import SimpleContentElement
from .WildcardType import WildcardType

logger = logging.getLogger(__name__)

@attribute(local_name='name', type=NCNameType)
@attribute(local_name='mixed', type=BooleanType, default=False)
@attribute(local_name='abstract', type=BooleanType, default=False)
@attribute(local_name='final', enum=['#all', 'extension', 'restriction'])
@attribute(local_name='block', enum=['#all', 'extension', 'restriction'])
@attribute(local_name='*', )
@element(local_name='simpleContent', list='tags', cls=SimpleContentElement, min=0, max=None)
@element(local_name='complexContent', list='tags', cls=ComplexContentElement, min=0, max=None)
@element(local_name='group', list='tags', cls=GroupType, min=0)
@element(local_name='all', list='tags',
    cls=('expatriate.model.xs.AllType', 'AllType'), min=0)
@element(local_name='choice', list='tags', cls=ChoiceElement, min=0)
@element(local_name='sequence', list='tags', cls=GroupType, min=0)
@element(local_name='attribute', list='tags', cls=AttributeType, min=0, max=None)
@element(local_name='attributeGroup', list='tags', cls=AttributeGroupType, min=0, max=None)
@element(local_name='anyAttribute', list='tags', cls=WildcardType, min=0)
class ComplexTypeType(AnnotatedType):
    # TODO .mixed & simpleContent sub-elements are mutulally exclusive

    def stub(self, path, schema):
        class_name = ''.join(cap_first(w) for w in self.name.split('_'))
        if not class_name.endswith('Type'):
            class_name = class_name + 'Type'

        super().stub(path, schema, class_name)
