# _*_ coding: utf-8 _*_
from plone import api
from plone.app.jsonfield import field
from plone.app.jsonfield import interfaces
from plone.app.jsonfield.compat import _
from plone.schemaeditor.fields import FieldFactory

import logging


__author__ = 'Md Nazrul Islam<email2nazrul@gmail.com>'

logger = logging.getLogger('plone.app.jsonfield')

# Patch: for plone 5.x
if api.env.plone_version().startswith('5'):
    import plone.app.dexterity.browser.types as padbt
    padbt.ALLOWED_FIELDS.append(u'plone.app.jsonfield.field.JSON')
    logger.info(
                'schemaeditor: patch done! `plone.app.jsonfield.field.JSON` is added in whitelist\n'
                'Location: plone.app.dexterity.browser.types.ALLOWED_FIELDS'
            )


class IJSON(interfaces.IJSON):
    """ """


JSONFieldFactory = FieldFactory(field.JSON, _(u'FHIR Resource Field'))
