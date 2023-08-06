# -*- coding: utf-8 -*-
from plone.app.jsonfield.field import JSON
from plone.app.jsonfield.interfaces import IJSON
from plone.supermodel.exportimport import BaseHandler
from plone.supermodel.interfaces import IToUnicode
from zope.component import adapter
from zope.interface import implementer

import six


__author__ = 'Md Nazrul Islam <email2nazrul@gmail.com>'


class JSONHandler_(BaseHandler):
    """Special handling for the JSONField field, to deal with 'default'
    that may be unicode.
    """

    # Don't read or write 'schema'
    filteredAttributes = BaseHandler.filteredAttributes.copy()
    filteredAttributes.update({'schema': 'rw'})

    def __init__(self, klass):
        super(JSONHandler_, self).__init__(klass)


@implementer(IToUnicode)
@adapter(IJSON)
class JSONToUnicode(object):

    def __init__(self, context):
        self.context = context

    def toUnicode(self, value):
        return six.text_type(value.stringify())


JSONHandler = JSONHandler_(JSON)
