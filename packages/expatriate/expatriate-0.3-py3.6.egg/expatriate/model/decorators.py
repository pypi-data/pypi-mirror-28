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

import functools
import importlib
import logging
import os
import sys
import types

from .AttributeMapper import AttributeMapper
from .ContentMapper import ContentMapper
from .ElementMapper import ElementMapper

logger = logging.getLogger(__name__)

def attribute(*args, **kwargs):
    '''
    Decorator to map xml elements to model children

    Used as follows::

        @attribute(local_name='test', type=StringType)
        class ModelWithTestAttribute(Model):
            pass

    :param str namespace: The xml namespace to match. It can also be * to match any namespace. If not specified, it defaults to the parent element's namespace.
    :param str local_name: Required. The local name of the xml attribute we're matching. It can also be * to match any local name.
    :param str into: The python attribute to store the value of the attribute into. Defaults to the local_name if not specified.
    :param type: The type of the expected value. Types are stored directly as data, no enclosed in a model class. Types usually restrict the domain values.
    :type type: class or tuple(package_str, class_str)
    :param enum: Enumeration the attribute's value must be from
    :type enum: list or tuple
    :param str pattern: Pattern which the value of the attribute must match.
    :param bool required: True or False (default). Specifies if the attribute is required.
    :param default: The default value of an attribute if it isn't specified. The (implicit) default is None or the first item of an *enum*.
    :param min: The minimum value of the attribute. Can be numeric or None (the default).
    :param max: The maximum value of the attribute. Can be numeric or None (the default).
    :param prohibited: The attribute should not appear in the element.
    '''
    def wrapper(cls):
        functools.update_wrapper(wrapper, cls)
        cls._add_attribute_mapper(AttributeMapper(**kwargs))

        return cls
    return wrapper

def element(*args, **kwargs):
    '''
    Decorator to map xml elements to model children.

    One of *type* or *cls* must be specified. If the type/class cannot be passed in
    by object, a tuple with the package and name of the class may be passed to
    defer the import of the class.

    Used as follows::

        @element(namespace='http://jaymes.biz/test', local_name='test',
            list='test', type=StringType)
        class ModelWithTestChildrenInAList(Model):
            pass

    :param namespace: The xml namespace to match. It can also be * to match any namespace. If not specified, it defaults to the parent element.
    :param local_name: Required. The local name of the xml element we're matching. It can also be * to match any local name.
    :param into: The python attribute to store the value of the element into. Defaults to the local_name if not specified.
    :param list: The python attribute to store the value of the element into (as a list).  Defaults to the local_name if not specified.
    :param dict: The python attribute to store the value of the element into (as a dict). Defaults to the local_name if not specified.
    :param dict_key: The attribute of the sub-element to use as the key of the dict. By default it is the *id* attribute.
    :param dict_value: The attribute of the sub-element to use as the value of the dict. By default it is the value of the element.
    :param type: The type of the expected value. Types are stored directly as data, no enclosed in a model class. Types usually restrict the domain values.
    :param cls: The model class with which to load the element.
    :param min: The minimum number of elements to be present. Can be numeric or None (the  default).
    :param max: The maximum number of elements to be present. Can be numeric or None (the default).
    :param enum: Enumeration to which the value of the element must belong.
    :param pattern: Pattern which the value of the element must match.
    :param nillable: If True, the element can be nil (from the xsi spec). False specifies that it cannot (the default).
    '''
    def wrapper(cls):
        functools.update_wrapper(wrapper, cls)
        cls._add_element_mapper(ElementMapper(**kwargs))

        return cls
    return wrapper

def content(*args, **kwargs):
    '''
    Decorator to map xml element content to model data.

    Used as follows::

        @content(enum=('value1', 'value2'))
        class Value1Or2(Model):
            pass

    :param enum: Enumeration the attribute's value must be from
    :param pattern: Pattern which the value of the attribute must match.
    :param type: Type against which a value must validate
    :param min: The minimum value of the attribute. Can be numeric or None (the default).
    :param max: The maximum value of the attribute. Can be numeric or None (the default).
    '''
    def wrapper(cls):
        functools.update_wrapper(wrapper, cls)
        cls._add_content_mapper(ContentMapper(**kwargs))

        return cls
    return wrapper
