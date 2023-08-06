# -*- coding: utf-8 -*-
from plone.app.jsonfield.interfaces import IJSON
from plone.rfc822.defaultfields import BaseFieldMarshaler
from zope.component import adapter
from zope.interface import Interface


@adapter(Interface, IJSON)
class JSONFieldMarshaler(BaseFieldMarshaler):
    """Field marshaler for plone.app.jsonfield values."""

    ascii = False

    def encode(self, value, charset='utf-8', primary=False):
        if value is None:
            return
        actual_value = value.stringify(prettify=True)
        return actual_value.encode(charset)

    def decode(self, value, message=None, charset='utf-8', contentType=None, primary=False):
        try:
            unicode_value = value.decode(charset)
        except UnicodeEncodeError:
            unicode_value = value  # was already unicode

        if unicode_value in ('', None):
            decoded_value = None
        else:
            decoded_value = IJSON(self.field).fromUnicode(unicode_value)
        return decoded_value

    def getContentType(self):
        value = self._query()
        if value is None:
            return None
        return 'application/json'

    def getCharset(self, default='utf-8'):
        value = self._query()
        if value is None:
            return None
        return getattr(value, '_encoding', default)
