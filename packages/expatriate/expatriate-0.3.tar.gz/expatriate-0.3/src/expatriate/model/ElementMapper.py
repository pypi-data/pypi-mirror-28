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

import importlib
import logging
import re

import expatriate
from publishsubscribe import PublishingDict, PublishingList

from .exceptions import *
from .Mapper import Mapper

logger = logging.getLogger(__name__)

class ElementMapper(Mapper):
    '''
        **kwargs**

        namespace
            The xml namespace to match. It can also be * to match any namespace.
            If not specified, it defaults to the parent element's namespace.
        local_name
            Required. The local name of the xml element we're matching. It can
            also be * to match any local name.

        into
            The python attribute to store the value of the element into.
            Defaults to the local_name if not specified.
        list
            The python attribute to store the value of the element into (as a
            list).  Defaults to the local_name if not specified.
        dict
            The python attribute to store the value of the element into (as a
            dict). Defaults to the local_name if not specified.

        dict_key
            The attribute of the sub-element to use as the key of the dict. By
            default it is the *id* attribute.
        dict_value
            The attribute of the sub-element to use as the value of the dict. By
            default it is the value of the element.

        Unless One of *type* or *cls* must be specified. *defer_class_load* can be
        used to load the class upon access instead of passing the class:

        type
            The type of the expected value. Types are stored directly as data,
            no enclosed in a model class. Types usually restrict the domain
            values.
        cls
            The model class with which to load the element.

        min
            The minimum number of elements to be present. Can be numeric or None
            (the  default).
        max
            The maximum number of elements to be present. Can be numeric or None
            (the default).

        enum
            Enumeration to which the value of the element must belong.
        pattern
            Pattern which the value of the element must match.

        nillable
            If True, the element can be nil (from the xsi spec). False
            specifies that it cannot (the default).
    '''

    def __init__(self, **kwargs):
        if 'local_name' not in kwargs:
            raise DecoratorException('Attributes need at least local_name defined')

        super().__init__(**kwargs)

    def get_attr_name(self):
        from .Model import Model

        if self._kwargs['local_name'] == Model.ANY_LOCAL_NAME:
            if 'into' not in self._kwargs:
                return '_elements'
            else:
                return self._kwargs['into']
        elif 'list' in self._kwargs:
            return self._kwargs['list']
        elif 'dict' in self._kwargs:
            return self._kwargs['dict']
        else:
            if 'into' in self._kwargs:
                return self._kwargs['into']
            else:
                return self._kwargs['local_name'].replace('-', '_')

    def initialize(self, model):
        from .Model import Model

        name = self.get_attr_name()

        if self._kwargs['local_name'] == Model.ANY_LOCAL_NAME:
            value = PublishingList()
            value.subscribe(model)
        elif 'list' in self._kwargs:
            value = PublishingList()
            value.subscribe(model)
        elif 'dict' in self._kwargs:
            value = PublishingDict()
            value.subscribe(model)
        else:
            value = None

        # initialze the attr if it doesn't exist
        if not hasattr(model, name):
            logger.debug('Initializing ' + str(self) + ' '+ name + ' to ' + str(value))
            setattr(model, name, value)

    def get_namespace(self):
        if 'namespace' in self._kwargs:
            return self._kwargs['namespace']
        else:
            return None

    def get_local_name(self):
        return self._kwargs['local_name']

    def find_reference_in(self, ref, model):
        from .Model import Model

        name = self.get_attr_name()
        attr = getattr(model, name)

        logger.debug('Looking for reference ' + ref + ' in ' + name + ' of ' + str(model))

        if isinstance(attr, list):
            for child in attr:
                try:
                    return child.find_reference(ref)
                except ReferenceException:
                    pass
        elif isinstance(attr, dict):
            for child in attr.values():
                try:
                    return child.find_reference(ref)
                except ReferenceException:
                    pass
        elif isinstance(attr, Model):
            return attr.find_reference(ref)

        raise ReferenceException('Could not find reference ' + ref
                + ' within ' + str(model) + '.' + name)

    def matches(self, el, model):
        from .Model import Model

        namespace = self.get_namespace()
        # if namespace is None:
        #     namespace = model.package_to_namespace(model.get_package())

        matches = (namespace, self.get_local_name()) in (
            (el.namespace, el.local_name),
            (None, el.local_name),
            (None, Model.ANY_LOCAL_NAME),
            (el.namespace, Model.ANY_LOCAL_NAME),
            (Model.ANY_NAMESPACE, Model.ANY_LOCAL_NAME)
        )

        if matches:
            logger.debug(str(self) + str((namespace, self.get_local_name())) + ' matches ' + str(el))
        else:
            logger.debug(str(self) + str((namespace, self.get_local_name())) + ' does not match ' + str(el))

        return matches

    def class_for_element(self, el, model):
        from .Model import Model

        if el.namespace is None:
            model_package = model.get_package()
        else:
            model_package = Model.namespace_to_package(el.namespace)

        if self.get_local_name() == Model.ANY_LOCAL_NAME:
            return Model.class_for_element(el)
        elif 'cls' in self._kwargs:
            return self._load_cls(self._kwargs['cls'])
        else:
            raise NotImplementedError

    def parse_in(self, model, el):
        from .Model import Model

        logger.debug('Parsing element ' + el.name + ' using kwargs: ' + str(self._kwargs))

        name = self.get_attr_name()

        if 'ignore' in self._kwargs and self._kwargs['ignore'] == True:
            logger.debug('Ignoring ' + name + ' element in ' + str(model))
            return

        if self._kwargs['local_name'] == Model.ANY_LOCAL_NAME:
            logger.debug(str(model) + ' parsing elements matching * into ' + name)

            lst = getattr(model, name)

            if el.is_nil():
                # check we can accept nil
                if 'nillable' not in self._kwargs or not self._kwargs['nillable']:
                    raise ValueError(str(el) + ' is nil, but not expecting nil value')
                value = None
            elif 'type' in self._kwargs:
                type_ = self._kwargs['type']()
                value = type_.parse_value(el.get_string_value())
            else:
                value = Model.load(model, el)

            lst.append(value)

            logger.debug('Appended ' + str(value) + ' to ' + name)

        elif 'list' in self._kwargs:
            logger.debug(str(model) + ' parsing ' + str(el) + ' elements into ' + name)

            lst = getattr(model, name)

            if el.is_nil():
                # check we can accept nil
                if 'nillable' not in self._kwargs or not self._kwargs['nillable']:
                    raise ValueError(str(el) + ' is nil, but not expecting nil value')
                value = None
            elif 'type' in self._kwargs:
                type_ = self._kwargs['type']
                value = el.get_string_value()
                value = type_().parse_value(value)
            else:
                value = Model.load(model, el)

            lst.append(value)

            logger.debug('Appended ' + str(value) + ' to ' + name)

        elif 'dict' in self._kwargs:
            logger.debug(str(model) + ' parsing ' + str(el) + ' elements into ' + name)

            dict_ = getattr(model, name)

            # TODO: implement key_element as well
            if 'dict_key' in self._kwargs:
                if self._kwargs['dict_key'] not in el.attributes:
                    key = None
                else:
                    key = el.attributes[self._kwargs['dict_key']]
            else:
                if 'id' not in el.attributes:
                    key = None
                else:
                    key = el.attributes['id']

            # TODO: implement value_element? as well
            if el.is_nil():
                # check we can accept nil
                if 'nillable' not in self._kwargs or not self._kwargs['nillable']:
                    raise ValueError(str(el) + ' is nil, but not expecting nil value')
                value = None
            elif 'dict_value' in self._kwargs:
                # TODO add ContentMapper
                # try parsing from an attribute
                if self._kwargs['dict_value'] not in el.attributes:
                    raise ValueError('Could not parse value from '
                        + str(el) + ' attribute '
                        + self._kwargs['dict_value'])

                if 'type' not in self._kwargs:
                    raise ValueError('Could not parse value from '
                        + str(el) + ' attribute '
                        + self._kwargs['dict_value']
                        + ' without explicit type')

                type_ = self._kwargs['type']()
                value = el.attributes[self._kwargs['dict_value']]
                value = type_.parse_value(value)

            else:
                # try parsing from the element itself, just mapping with the key
                if 'type' in self._kwargs:
                    type_ = self._kwargs['type']()
                    value = type_.parse_value(el.get_string_value())
                else:
                    # needs 'cls' in self._kwargs
                    value = Model.load(model, el)

            dict_[key] = value

            logger.debug('Mapped ' + str(key) + ' to ' + str(value) + ' in ' + name)

        elif 'cls' in self._kwargs:
            logger.debug(str(model) + ' parsing ' + str(el) + ' element as '
                + str(self._kwargs['cls']))

            if el.is_nil():
                # check we can accept nil
                if 'nillable' not in self._kwargs or not self._kwargs['nillable']:
                    raise ValueError(str(el) + ' is nil, but not expecting nil value')
                value = None
            else:
                value = Model.load(model, el)

            setattr(model, name, value)

            logger.debug('Set attribute ' + str(name) + ' to ' + str(value)
                + ' in ' + str(model))

        elif 'type' in self._kwargs:
            logger.debug(str(model) + ' parsing ' + str(el) + ' elements as '
                + self._kwargs['type'])

            if el.is_nil():
                # check we can accept nil
                if 'nillable' not in self._kwargs or not self._kwargs['nillable']:
                    raise ValueError(str(el) + ' is nil, but not expecting nil value')
                value = None
            else:
                type_ = self._kwargs['type']
                # load from a tuple (module_name, class_name) to defer class load
                if isinstance(type_, tuple):
                    mod = importlib.import_module(type_[0])
                    type_ = getattr(mod, type_[1])
                value = el.get_string_value()
                value = type_().parse_value(value)

            setattr(model, name, value)

            logger.debug('Set attribute ' + str(name) + ' to ' + str(value)
                + ' in ' + str(model))

        elif 'enum' in self._kwargs:
            logger.debug(str(model) + ' parsing ' + str(el)
                + ' elements from enum ' + str(self._kwargs['enum']))

            value = el.get_string_value()
            if value not in self._kwargs['enum']:
                raise EnumerationException(str(el)
                    + ' value must be one of ' + str(self._kwargs['enum']))

            setattr(model, name, value)

            logger.debug('Set enum attribute ' + str(name) + ' to '
                + str(value) + ' in ' + str(model))

        elif 'pattern' in self._kwargs:
            logger.debug(str(model) + ' parsing ' + str(el)
                + ' elements from pattern ' + str(self._kwargs['pattern']))

            value = el.get_string_value()
            if re.match(self._kwargs['pattern'], value) is None:
                raise PatternException(str(el)
                    + ' value must match ' + str(self._kwargs['pattern']))

            setattr(model, name, value)

            logger.debug('Set pattern attribute ' + str(name) + ' to '
                + str(value) + ' in ' + str(model))

        else:
            raise UnknownElementException(str(model) + ' could not parse '
                + str(el) + ' element')

    def validate(self, model):
        from .Model import Model

        name = self.get_attr_name()

        min_ = 1
        if (
            'dict' in self._kwargs
            or 'list' in self._kwargs
            or self.get_local_name() == Model.ANY_LOCAL_NAME
        ):
            count = len(getattr(model, name))
            # dicts and lists default to no max
            max_ = None
        else:
            max_ = 1
            count = 1

        # if there's an explicit min/max definition, use that
        if 'min' in self._kwargs:
            min_ = self._kwargs['min']
        if 'max' in self._kwargs:
            max_ = self._kwargs['max']

        # check that we have the min & max of those elements
        if min_ != 0 and count < min_:
            raise MinimumElementException(str(model)
                + ' must have at least ' + str(min_) + ' '
                + str((self.get_namespace(), self.get_local_name()))
                + ' elements')

        if max_ is not None and count > max_:
            raise MaximumElementException(str(model)
                + ' may have at most ' + str(max_) + ' '
                + str((self.get_namespace(), self.get_local_name()))
                + ' elements')

    def setattr(self, model, name, value):
        from .Model import Model

        if not hasattr(model, '_initialized'):
            object.__setattr__(model, name, value)
            return

        if (
            'list' in self._kwargs
            or self.get_local_name() == Model.ANY_LOCAL_NAME
        ):
            # wrap in PublishingList; updates are captured via Publisher
            object.__setattr__(model, name, PublishingList(value))
        elif 'dict' in self._kwargs:
            # wrap in PublishingDict; updates are captured via Publisher
            object.__setattr__(model, name, PublishingDict(value))
        else:
            old_value = getattr(model, name)
            object.__setattr__(model, name, value)
            if old_value is None and value is None:
                pass
            elif old_value is None and value is not None:
                model.data_added(value, None, value)
            elif old_value is not None and value is None:
                model.data_deleted(value, None, value)
            else: # old_value is not None and value is not None
                model.data_updated(value, None, old_value, value)

    def produce_in(self, el, model, id_):
        from .Model import Model

        name = self.get_attr_name()
        attr = getattr(model, name)
        if id_ is None:
            value = attr
        else:
            value = attr[id_]

        logger.debug(str(self) + ' producing ' + str(model) + ' element '
            + name  + str([id_]) + ' according to ' + str(self._kwargs))

        if hasattr(value, '_namespace') and value._namespace is not None:
            namespace = value._namespace
        elif 'namespace' in self._kwargs:
            if self._kwargs['namespace'] == Model.ANY_NAMESPACE:
                raise ElementMappingException(str(self) + ' cannot map '
                    + str(model) + '.' + name + ' without a namespace override')
            namespace = self._kwargs['namespace']
        else:
            namespace = el.namespace

        if hasattr(value, '_prefix') and value._prefix is not None:
            prefix = value._prefix
        else:
            prefix = el.namespace_to_prefix(namespace)

        if hasattr(value, '_local_name') and value._local_name is not None:
            local_name = value._local_name
        else:
            if self._kwargs['local_name'] == Model.ANY_LOCAL_NAME:
                raise ElementMappingException(str(self) + ' cannot map '
                    + str(model) + '.' + name + ' without a local_name override')
            local_name = self._kwargs['local_name']

        if local_name is None:
            raise ElementMappingException('local_name must be defined by constructor or @element')

        if self._kwargs['local_name'] == Model.ANY_LOCAL_NAME:
            if value is None:
                return

            el.append(value.produce(parent_el=el))
        elif 'list' in self._kwargs:
            if 'type' in self._kwargs:
                if value is None:
                    sub_el = expatriate.Element(local_name, namespace=namespace, prefix=prefix, parent=el)
                    sub_el.attributes['xmlns:xsi'] = 'http://www.w3.org/2001/XMLSchema-instance'
                    sub_el.attributes['xsi:nil'] = 'true'
                    el.append(sub_el)
                else:
                    # wrap value in xs element
                    class_ = self._kwargs['type']
                    child = class_(local_name=local_name, namespace=namespace, prefix=prefix)
                    child.set_value(value)
                    el.append(child.produce(parent_el=el))
            elif 'cls' in self._kwargs:
                if value is None:
                    sub_el = expatriate.Element(local_name, namespace=namespace, prefix=prefix, parent=el)
                    sub_el.attributes['xmlns:xsi'] = 'http://www.w3.org/2001/XMLSchema-instance'
                    sub_el.attributes['xsi:nil'] = 'true'
                    el.append(sub_el)
                elif not isinstance(value, self._load_cls(self._kwargs['cls'])):
                    raise ElementMappingException('Value ' + str(value)
                        + ' is not of the expected class: '
                        + str(self._kwargs['cls']))
                else:
                    el.append(value.produce(parent_el=el))

            else:
                raise ElementMappingException('"cls" or "type" must be '
                    + 'defined for "list" model mapping')

        elif 'dict' in self._kwargs:
            # TODO: implement key_element as well
            if 'dict_key' in self._kwargs:
                key_name = self._kwargs['dict_key']
            else:
                key_name = 'id'

            if 'type' in self._kwargs:
                sub_el = expatriate.Element(local_name, namespace=namespace, prefix=prefix, parent=el)
                sub_el.attributes[key_name] = id_
                if 'dict_value' in self._kwargs:
                    if value is None:
                        raise ValueError(str(self)
                            + ' Cannot have none for a dict_value: '
                            + self._kwargs['dict'] + '[' + id_ + ']')
                    type_ = self._kwargs['type']()
                    value = type_.produce_value(value)
                    sub_el.attributes[self._kwargs['dict_value']] = value
                else:
                    if value is None:
                        sub_el.attributes['xmlns:xsi'] = 'http://www.w3.org/2001/XMLSchema-instance'
                        sub_el.attributes['xsi:nil'] = 'true'
                    else:
                        type_ = self._kwargs['type']()
                        sub_el.children.append(expatriate.CharacterData(type_.produce_value(value)))
                el.append(sub_el)

            elif 'cls' in self._kwargs:
                if value is None:
                    sub_el = expatriate.Element(local_name, namespace=namespace, prefix=prefix, parent=el)
                    sub_el.attributes[key_name] = id_
                    sub_el.attributes['xmlns:xsi'] = 'http://www.w3.org/2001/XMLSchema-instance'
                    sub_el.attributes['xsi:nil'] = 'true'
                    el.append(sub_el)
                else:
                    setattr(value, key_name, id_)
                    el.append(value.produce(parent_el=el))

            else:
                raise ValueError('"class" or "type" must be defined for "dict" model mapping')

        elif 'cls' in self._kwargs:
            if value is None:
                return

            el.append(value.produce(parent_el=el))

        elif 'type' in self._kwargs:
            if value is None:
                return

            class_ = self._kwargs['type']
            child = class_(local_name=local_name, namespace=namespace, prefix=prefix)
            child.set_value(value)

            el.append(child.produce(parent_el=el))

        elif 'enum' in self._kwargs:
            if value is None:
                return

            if value not in self._kwargs['enum']:
                raise EnumerationException(str(namespace, local_name)
                    + ' value must be one of ' + str(self._kwargs['enum'])
                    + ': ' + str(value))

            child = StringType(local_name=local_name, namespace=namespace, prefix=prefix)
            child.set_value(value)

            el.append(child.produce(parent_el=el))

        else:
            raise UnknownElementException(str(self) + ' could not produce ' + str(namespace, local_name) + ' element')
