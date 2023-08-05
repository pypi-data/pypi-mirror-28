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

XML_SPACE_ENUMERATION = (
    'default',
    # The value "default" signals that applications' default white-space
    # processing modes are acceptable for this element
    'preserve',
    # the value "preserve" indicates the intent that applications preserve all
    # the white space
)
''' Enumeration of the possible whitespace processing modes '''

from .exceptions import *
from .xpath import *
from .Attribute import Attribute
from .CharacterData import CharacterData
from .Comment import Comment
from .Document import Document
from .Element import Element
from .Namespace import Namespace
from .ProcessingInstruction import ProcessingInstruction
