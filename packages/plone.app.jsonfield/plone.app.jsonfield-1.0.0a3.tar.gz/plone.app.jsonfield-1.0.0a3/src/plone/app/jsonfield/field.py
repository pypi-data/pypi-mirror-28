# _*_ coding:utf-8 _*_
from plone import api
from plone.app.jsonfield.compat import _
from plone.app.jsonfield.compat import json
from plone.app.jsonfield.helpers import parse_json_str
from plone.app.jsonfield.interfaces import IJSON
from plone.app.jsonfield.interfaces import IJSONValue
from plone.app.jsonfield.value import JSONArrayValue
from plone.app.jsonfield.value import JSONObjectValue
from plone.app.jsonfield.value import JSONValue
from zope.interface import implementer
from zope.interface import Invalid
from zope.schema import Object
from zope.schema.interfaces import IFromUnicode
from zope.schema.interfaces import WrongType

import six
import sys


__author__ = 'Md Nazrul Islam<nazrul@zitelab.dk>'


@implementer(IJSON, IFromUnicode)
class JSON(Object):
    """JSON field"""
    _type = JSONValue
    schema = IJSONValue

    def __init__(self, json_schema=None, **kw):
        """
        :param: json_schema: JSON Schema http://json-schema.org/
        """
        self.json_schema = json_schema
        self.init_validate()

        if 'default' in kw:
            default = kw['default']
            if isinstance(default, six.string_types):
                kw['default'] = self.fromUnicode(default)
            elif isinstance(default, dict):
                kw['default'] = self.from_iterable(default)

        super(JSON, self).__init__(schema=self.schema, **kw)

    def fromUnicode(self, str_val):
        """ """
        json_dict = parse_json_str(str_val)

        return self.from_iterable(json_dict)

    def from_iterable(self, iter_value):
        """ """
        if iter_value is None:
            value = None
        else:
            value = self._from_iterable(iter_value)
        # do validation now
        self.validate(value)
        return value

    def init_validate(self):
        """ """
        schema = self.json_schema
        if schema is None:
            # No validation is required.
            return

        try:
            if isinstance(schema, six.string_types):
                schema = json.loads(schema)
                self.json_schema = schema

            json.dumps(schema)
            if not isinstance(schema, dict):
                raise WrongType(
                    'Schema value must be dict type! but got `{0!s}` type'.format(type(self.json_schema)))

        except (ValueError, TypeError) as exc:
            msg = _('Invalid schema data type! dict data type is expected.')
            if api.env.debug_mode():
                msg += _('Original Exception: {0!s}').format(exc)
            six.reraise(Invalid, Invalid(msg), sys.exc_info()[2])

    def _from_iterable(self, iter_value):
        """ """
        factory = JSONObjectValue
        if isinstance(iter_value, (list, tuple, set)):
            factory = JSONArrayValue

        value = factory(iter_value, schema=self.json_schema, encoding='utf-8')

        return value
