# -*- coding: utf-8 -*-
"""Module where all interfaces, events and exceptions live."""
from plone.app.jsonfield.compat import _
from zope import schema as zs
from zope.interface import Interface
from zope.schema.interfaces import IObject


class IJSON(IObject):
    """ """
    json_schema = zs.Iterable(
        title=_('JSON schema'),
        required=False
    )

    def from_iterable(iter_value):
        """ """


class IJSONValue(Interface):
    """ """
    def stringify(prettify=False):
        """Transformation to JSON string representation"""

    def patch(patch_data):
        """JSON Patch implementation: https://tools.ietf.org/html/rfc6902"""
