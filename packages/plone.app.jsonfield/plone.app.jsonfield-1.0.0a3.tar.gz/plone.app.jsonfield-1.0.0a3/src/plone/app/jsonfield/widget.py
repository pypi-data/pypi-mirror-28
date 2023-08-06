# _*_ coding: utf-8 _*_
from plone.app.jsonfield.interfaces import IJSON
from plone.app.jsonfield.interfaces import IJSONValue
from z3c.form.browser.textarea import TextAreaWidget
from z3c.form.browser.widget import addFieldClass
from z3c.form.converter import BaseDataConverter
from z3c.form.interfaces import IFieldWidget
from z3c.form.interfaces import IFormLayer
from z3c.form.interfaces import ITextAreaWidget
from z3c.form.interfaces import NOVALUE
from z3c.form.widget import FieldWidget
from zope.component import adapter
from zope.interface import implementer
from zope.interface import implementer_only

import six


__author__ = 'Md Nazrul Islam<email2nazrul@gmail.com>'


class IJSONWidget(ITextAreaWidget):
    """ """


@implementer_only(IJSONWidget)
class JSONWidget(TextAreaWidget):

    klass = u'JSONWidget'
    value = None

    def update(self):
        super(JSONWidget, self).update()
        addFieldClass(self)

    def extract(self, default=NOVALUE):
        raw = self.request.get(self.name, default)
        return raw


@adapter(IJSON, IFormLayer)
@implementer(IFieldWidget)
def JSONFieldWidget(field, request):
    """IFieldWidget factory for JSONWidget."""
    return FieldWidget(field, JSONWidget(request))


class JSONConverter(BaseDataConverter):
    """Data converter for the JSONWidget
    """

    def toWidgetValue(self, value):
        if IJSONValue.providedBy(value):
            return value

        elif value in (NOVALUE, None, ''):
            return ''

        elif isinstance(value, six.string_types):
            return IJSON(self.field).fromUnicode(value)

        raise ValueError(
            'Can not convert {0!s} to an IJSONValue'.format(value)
        )

    def toFieldValue(self, value):
        """ """
        if IJSONValue.providedBy(value):
            return value

        elif isinstance(value, six.string_types):
            return IJSON(self.field).fromUnicode(value)

        elif value in (NOVALUE, None, ''):
            return None

        raise ValueError(
            'Can not convert {0!s} to an IJSONValue'.format(value)
        )


class JSONAreaConverter(BaseDataConverter):
    """Data converter for the original z3cform TextWidget"""

    def toWidgetValue(self, value):
        """ """
        if value in (None, '', NOVALUE):
            return ''

        if IJSONValue.providedBy(value):
            if self.widget.mode in ('input', 'hidden'):
                return value.stringify()
            elif self.widget.mode == 'display':
                return value.stringify()

        if isinstance(value, six.string_types):
            return value

        raise ValueError(
            'Can not convert {0:s} to unicode'.format(repr(value))
        )

    def toFieldValue(self, value):
        """ """
        if IJSONValue.providedBy(value):
            return value

        elif isinstance(value, six.string_types):
            return IJSON(self.field).fromUnicode(value)

        elif value in (NOVALUE, None, ''):
            return None

        raise ValueError(
            'Can not convert {0!r} to an IJSONValue'.format(value)
        )
