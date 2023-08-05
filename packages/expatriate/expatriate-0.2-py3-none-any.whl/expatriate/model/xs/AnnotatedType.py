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
import os

from ..decorators import *
from .AnnotationElement import AnnotationElement
from .AnyTypeType import AnyTypeType
from .IdType import IdType

logger = logging.getLogger(__name__)

@attribute(local_name='id', type=IdType)
@element(local_name='annotation', list='tags', cls=AnnotationElement, min=0)
class AnnotatedType(AnyTypeType):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self._super_module = 'expatriate.model.Model'
        self._super_class = 'Model'
        self._value_enumeration = None
        self._value_pattern = None

    def set_super_module(self, super_module):
        self._super_module = super_module

    def set_super_class(self, super_class):
        self._super_class = super_class

    def append_value_enumeration(self, value):
        if self._value_enumeration is None:
            self._value_enumeration = []
        self._value_enumeration.append(value)

    def set_value_pattern(self, pattern):
        self._value_pattern = pattern

    def stub(self, path, schema, class_name):
        model_map = {'elements': [], 'attributes': {}}
        for t in self.tags:
            defs = t.get_defs(schema, self)
            model_map['elements'].extend(defs['elements'])
            model_map['attributes'].update(defs['attributes'])

        logger.debug('Stubbing ' + str(self) + ' to ' + class_name + '.py')

        with open(os.path.join(path, class_name + '.py'), 'w') as f:
            f.write(STUB_HEADER)
            f.write('import logging\n\n')
            f.write('from ' + self._super_module + ' import ' + self._super_class + '\n\n')
            f.write('logger = logging.getLogger(__name__)\n')
            f.write('class ' + class_name + '(' + self._super_class + '):\n')

            indent = 4

            f.write((' ' * indent) + "MODEL_MAP = {\n")
            indent += 4

            f.write((' ' * indent) + "'elements': [\n")
            indent += 4
            for el_def in model_map['elements']:
                f.write((' ' * indent) + str(el_def) + ",\n")
            indent -= 4
            f.write((' ' * indent) + "],\n")

            f.write((' ' * indent) + "'attributes': {\n")
            indent += 4
            for name, att_def in model_map['attributes']:
                f.write((' ' * indent) + "'" + name + "': " + str(att_def) + ",\n")
            indent -= 4
            f.write((' ' * indent) + "},\n")

            indent -= 4
            f.write((' ' * indent) + "}\n\n")

            if self._value_enumeration is not None:
                f.write((' ' * indent) + "def get_value_enum(self):\n")
                indent += 4
                f.write((' ' * indent) + "return [\n")
                indent += 4
                for v in self._value_enumeration:
                    f.write((' ' * indent) + repr(v) + ",\n")
                indent -= 4
                f.write((' ' * indent) + "]\n\n")
                indent -= 4

            if self._value_pattern is not None:
                f.write((' ' * indent) + "def get_value_pattern(self):\n")
                indent += 4
                f.write((' ' * indent) + "return r'" + self._value_pattern + "'\n\n")
                indent -= 4
