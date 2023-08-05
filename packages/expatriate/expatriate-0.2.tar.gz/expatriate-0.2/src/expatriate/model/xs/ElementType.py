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

from . import FORM_CHOICE_ENUMERATION
from ..decorators import *
from .AllNniType import AllNniType
from .AnnotatedType import AnnotatedType
from .BooleanType import BooleanType
from .ComplexTypeType import ComplexTypeType
from .KeybaseType import KeybaseType
from .KeyRefElement import KeyRefElement
from .NCNameType import NCNameType
from .NonNegativeIntegerType import NonNegativeIntegerType
from .QNameType import QNameType
from .SimpleTypeType import SimpleTypeType
from .StringType import StringType

logger = logging.getLogger(__name__)

@element(local_name='simpleType', list='tags', cls=SimpleTypeType, min=0)
@element(local_name='complexType', list='tags', cls=ComplexTypeType, min=0)
@element(local_name='unique', list='tags', cls=KeybaseType, min=0, max=None)
@element(local_name='key', list='tags', cls=KeybaseType, min=0, max=None)
@element(local_name='keyref', list='tags', cls=KeyRefElement, min=0, max=None)
@attribute(local_name='name', type=NCNameType)
@attribute(local_name='ref', type=QNameType)
@attribute(local_name='type', type=QNameType)
@attribute(local_name='substitutionGroup', type=QNameType)
@attribute(local_name='default', type=StringType)
@attribute(local_name='fixed', type=StringType)
@attribute(local_name='nillable', type=BooleanType, default=False)
@attribute(local_name='abstract', type=BooleanType, default=False)
@attribute(local_name='final', enum=['#all', 'extension', 'restriction'])
@attribute(local_name='block', enum=['#all', 'extension', 'restriction', 'substitution'])
@attribute(local_name='form', enum=FORM_CHOICE_ENUMERATION)
@attribute(local_name='minOccurs', type=NonNegativeIntegerType, default=1)
@attribute(local_name='maxOccurs', type=AllNniType, default=1)
@attribute(local_name='*')
class ElementType(AnnotatedType):
    def stub(self, path, schema):
        class_name = ''.join(cap_first(w) for w in self.name.split('_'))
        if not class_name.endswith('Element'):
            class_name = class_name + 'Element'
        schema.add_tag_mapping(self.name, class_name)

        super().stub(path, schema, class_name)

    def get_defs(self, schema, top_level):
        if self.ref is not None:
            return schema.find_reference(self.ref).get_defs(schema, top_level)

        model_map = {'elements': [], 'attributes': {}}

        e = {}

        e['min'] = self.minOccurs

        if self.maxOccurs == 'unbounded':
            e['max'] = None
        else:
            e['max'] = self.maxOccurs

        if self.default is not None:
            e['default'] = self.default

        if self.nillable:
            e['nillable'] = True

        # TODO type vs. class detection
        e['class'] = self.type

        if self.maxOccurs == 'unbounded':
            e['list'] = self.name + 's'

        e['tag_name'] = self.name

        model_map['elements'].append(e)
        logger.debug('Adding element ' + str(e))

        for t in self.tags:
            defs = t.get_defs(schema, top_level)
            model_map['elements'].extend(defs['elements'])
            model_map['attributes'].update(defs['attributes'])
        return model_map
