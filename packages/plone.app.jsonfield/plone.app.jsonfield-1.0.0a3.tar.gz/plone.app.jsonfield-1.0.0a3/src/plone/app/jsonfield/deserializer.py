# _*_ coding: utf-8 _*_
from plone.app.jsonfield.interfaces import IJSON
from plone.dexterity.interfaces import IDexterityContent
from plone.restapi.deserializer.dxfields import DefaultFieldDeserializer
from plone.restapi.interfaces import IFieldDeserializer
from zope.component import adapter
from zope.interface import implementer
from zope.publisher.interfaces.browser import IBrowserRequest

import six


__author__ = 'Md Nazrul Islam <email2nazrul@gmail.com>'


@implementer(IFieldDeserializer)
@adapter(IJSON, IDexterityContent, IBrowserRequest)
class JSONDeserializer(DefaultFieldDeserializer):

    def __call__(self, value):
        """ """
        if isinstance(value, six.string_types):
            return IJSON(self.field).fromUnicode(value)
        elif isinstance(value, dict):
            return IJSON(self.field).from_iterable(value)
        else:
            raise ValueError(
                'Invalid data type({0}) provided! only dict or string data type is accepted.'.format(type(value))
            )
