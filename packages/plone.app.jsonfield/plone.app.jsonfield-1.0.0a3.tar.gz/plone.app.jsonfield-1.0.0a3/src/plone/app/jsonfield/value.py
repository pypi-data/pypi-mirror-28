# _*_ coding: utf-8 _*_
from .compat import EMPTY_STRING
from .compat import NO_VALUE
from .interfaces import IJSONValue
from plone import api
from plone.app.jsonfield.compat import _
from plone.app.jsonfield.compat import json
from zope.interface import implementer
from zope.interface import Invalid
from zope.schema.interfaces import WrongType

import jsonpatch
import jsonschema
import six
import sys


__author__ = 'Md Nazrul Islam<email2nazrul@gmail.com>'


@implementer(IJSONValue)
class JSONValue(object):
    """"""
    def patch(self, patch_data):
        """:@links: https://python-json-patch.readthedocs.io/en/latest/tutorial.html#creating-a-patch"""
        if not isinstance(patch_data, (list, tuple)):
            raise WrongType('patch value must be list or tuple type! but got `{0}` type.'.format(type(patch_data)))

        try:
            patcher = jsonpatch.JsonPatch(patch_data)
            # Pacther is doing deepcopy!
            new_value = patcher.apply(self)
            # Let's update
            self.update(new_value)

        except (jsonpatch.JsonPatchException, jsonpatch.JsonPointerException) as e:
            six.reraise(Invalid, Invalid(str(e)), sys.exc_info()[2])

    def stringify(self, prettify=False):
        """ """
        params = {}
        params['encoding'] = 'utf-8'
        if prettify:
            # will make little bit slow, so apply only if needed
            params['indent'] = 4

        return json.dumps(self, **params)

    def _validate_object(self, obj, schema=None):
        """ """
        if obj in (None, NO_VALUE, EMPTY_STRING):
            return True

        if isinstance(obj, six.string_types):
            raise WrongType('value must be json serialable!')

        try:
            # Test if value is iterable
            iter(obj)
            json.dumps(obj)
        except (TypeError, ValueError) as exc:
            msg = _('Only dict or list type value is allowed, value must be json serialable!')
            if api.env.debug_mode():
                msg += _('Original exception: {0!s}').format(exc)

            six.reraise(WrongType, WrongType(msg), sys.exc_info()[2])

        if schema:
            try:
                jsonschema.validate(obj, schema)
            except (
                    jsonschema.ErrorTree,
                    jsonschema.ValidationError,
                    jsonschema.SchemaError,
                    jsonschema.FormatError,
                    jsonschema.RefResolutionError
                    ) as exc:
                six.reraise(Invalid, Invalid(str(exc)), sys.exc_info()[2])

    def __init__(self, obj, schema=None, encoding='utf-8'):
        """ """
        # Let's validate before value assignment!
        self._validate_object(obj, schema=schema)
        self.encoding = encoding
        args = []
        if obj not in (None, NO_VALUE, EMPTY_STRING):
            args.append(obj)

        super(JSONValue, self).__init__(*args)

    def __str__(self):
        """ """
        return self.stringify()


class JSONObjectValue(JSONValue, dict):
    """ """
    def _validate_object(self, obj, schema=None):
        """" """
        res = super(JSONObjectValue, self)._validate_object(obj, schema)
        if not res:
            if isinstance(obj, (list, tuple, set)):
                raise WrongType('given value must be dict type data but got `{0}` type data!'.format(type(obj)))
        return res


class JSONArrayValue(JSONValue, list):
    """" """
    def patch(self, patch_data):
        raise Invalid('json patch is not applicable on array type value!')

    def _validate_object(self, obj, schema=None):
        """ """
        res = super(JSONArrayValue, self)._validate_object(obj, schema)
        if not res:
            if not isinstance(obj, (list, tuple, set)):
                raise WrongType('given value must be array type data but got `{0}` type data!'.format(type(obj)))
        return res


__all__ = [str(x) for x in ('JSONObjectValue', 'JSONArrayValue', )]
