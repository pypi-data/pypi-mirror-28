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
from .AttributeGroupType import AttributeGroupType
from .AttributeType import AttributeType
from .ChoiceElement import ChoiceElement
from .GroupType import GroupType
from .QNameType import QNameType
from .WildcardType import WildcardType

logger = logging.getLogger(__name__)

@attribute(local_name='base', type=QNameType, required=True)
@element(local_name='group', list='tags', cls=GroupType, min=0)
@element(local_name='all', list='tags',
    cls=('expatriate.model.xs.AllType', 'AllType'),
    min=0)
@element(local_name='choice', list='tags', cls=ChoiceElement, min=0)
@element(local_name='sequence', list='tags', cls=GroupType, min=0)
@element(local_name='attribute', list='tags', cls=AttributeType, min=0, max=None)
@element(local_name='attributeGroup', list='tags', cls=AttributeGroupType, min=0, max=None)
@element(local_name='anyAttribute', list='tags', cls=WildcardType, min=0)
class ExtensionType(AnnotatedType):
    def get_defs(self, schema, top_level):
        logger.debug('Base: ' + self.base)
        # TODO unable to map xmlns because ET doesn't retain it
        base_ns, base_name = [self.base.partition(':')[i] for i in [0,2]]
        top_level.set_super_module(base_ns)
        top_level.set_super_class(base_name)

        return super().get_defs(schema, top_level)
