# _*_ coding: utf-8 _*_
from __future__ import print_function  # noqa: I001
from . import FHIR_FIXTURE_PATH
from .schema import ITestToken
from plone.app.jsonfield import widget
from plone.app.jsonfield.testing import PLONE_APP_JSON_FIELD_FUNCTIONAL_TESTING
from plone.app.jsonfield.testing import PLONE_APP_JSON_FIELD_INTEGRATION_TESTING
from plone.app.testing import SITE_OWNER_NAME
from plone.app.testing import SITE_OWNER_PASSWORD
from plone.testing import z2
from z3c.form.interfaces import IDataConverter
from z3c.form.interfaces import IFieldWidget
from z3c.form.interfaces import NOVALUE
from zope.component import queryMultiAdapter
from zope.publisher.browser import TestRequest
from zope.schema import getFields

import json
import os
import unittest


___author__ = 'Md Nazrul Islam<email2nazrul@gmail.com>'


class WidgetIntegrationTest(unittest.TestCase):
    """ """
    layer = PLONE_APP_JSON_FIELD_INTEGRATION_TESTING

    def setUp(self):
        """ """
        self.portal = self.layer['portal']
        self.request = self.layer['request']

    def test_widget(self):
        """ """
        with open(os.path.join(FHIR_FIXTURE_PATH, 'Organization.json'), 'r') as f:
            json_object_str = f.read()

        request = TestRequest(form={'resource': json_object_str})
        json_widget = widget.JSONWidget(request)
        json_widget.name = 'resource'

        self.assertTrue(widget.IJSONWidget.providedBy(json_widget))
        self.assertIsNone(json_widget.value)
        json_widget.update()

        self.assertEqual(json_widget.value, json_object_str)
        json_field = getFields(ITestToken)['resource']

        field_widget = widget.JSONFieldWidget(json_field, request)
        self.assertTrue(IFieldWidget.providedBy(field_widget))
        # @TODO: Make sure widget.render() works!

    def test_data_converter(self):
        """ """
        with open(os.path.join(FHIR_FIXTURE_PATH, 'Organization.json'), 'r') as f:
            json_object_str = f.read()
        request = TestRequest(form={'resource': json_object_str})
        json_field = getFields(ITestToken)['resource']
        field_widget = widget.JSONFieldWidget(json_field, request)

        converter = queryMultiAdapter((json_field, field_widget), IDataConverter)
        self.assertIsNotNone(converter)

        # All Test: toWidgetValue
        json_value = converter.toWidgetValue('')
        self.assertFalse(json_value)
        self.assertEqual(json_value, '')

        json_value = converter.toWidgetValue(json_object_str)

        self.assertIn(json_value['resourceType'], json_object_str.decode('utf-8'))

        try:
            converter.toWidgetValue(('hello', 'wrong type', ))
            raise AssertionError('Code should not come here! As wrong types data is provided')
        except ValueError as exc:
            self.assertIn('IJSONValue', str(exc))

        # All Test: toFieldValue
        json_value = converter.toFieldValue(NOVALUE)
        self.assertFalse(json_value)
        self.assertIsNone(json_value)

        json_value = converter.toFieldValue(json_object_str)
        self.assertIn(json_value['resourceType'], json_object_str.decode('utf-8'))

        json_value2 = converter.toFieldValue(json_value)
        self.assertEqual(json_value, json_value2)

        try:
            converter.toFieldValue(('hello', 'wrong type', ))
            raise AssertionError('Code should not come here! As wrong types data is provided')
        except ValueError as exc:
            self.assertIn('IJSONValue', str(exc))

    def test_textarea_data_converter(self):
        """ """
        from z3c.form.browser.textarea import TextAreaWidget

        with open(os.path.join(FHIR_FIXTURE_PATH, 'Organization.json'), 'r') as f:
            json_object_str = f.read()
        request = TestRequest(form={'resource': json_object_str})
        json_field = getFields(ITestToken)['resource']
        field_widget = TextAreaWidget(request)

        converter = queryMultiAdapter((json_field, field_widget), IDataConverter)
        self.assertIsNotNone(converter)

        # All Test: toFieldValue
        json_value_empty = converter.toFieldValue(NOVALUE)
        self.assertFalse(json_value_empty)

        json_value = converter.toFieldValue(json_object_str)
        self.assertIn(json_value['resourceType'], json_object_str.decode('utf-8'))

        json_value2 = converter.toFieldValue(json_value)
        self.assertEqual(json_value, json_value2)

        try:
            converter.toFieldValue(('hello', 'wrong type', ))
            raise AssertionError('Code should not come here! As wrong types data is provided')
        except ValueError as exc:
            self.assertIn('IJSONValue', str(exc))

        # All Test: toWidgetValue
        original_mode = converter.widget.mode
        converter.widget.mode = 'display'
        json_object_str = converter.toWidgetValue(json_value)
        self.assertEqual(len(json_object_str), len(json_value.stringify()))

        converter.widget.mode = original_mode

        json_value = converter.toWidgetValue('')
        self.assertFalse(json_value)
        self.assertEqual(json_value, '')

        json_value_1 = converter.toWidgetValue(json_object_str)
        self.assertIn('Organization', json_value_1)
        self.assertIn('resourceType', json_value_1)

        json_value_2 = converter.toWidgetValue(json_value2)
        self.assertEqual(json.loads(json_value_1), json.loads(json_value_2))

        json_value_3 = converter.toWidgetValue(json_value_empty)
        self.assertEqual(json_value_3, '')

        try:
            converter.toWidgetValue(('hello', 'wrong type', ))
            raise AssertionError('Code should not come here! As wrong types data is provided')
        except ValueError as exc:
            self.assertIn('Can not convert', str(exc))


class WidgetFunctionalTest(unittest.TestCase):
    """ """
    layer = PLONE_APP_JSON_FIELD_FUNCTIONAL_TESTING

    def setUp(self):
        """ """
        self.portal = self.layer['portal']
        self.portal_url = self.portal.absolute_url()
        self.browser = z2.Browser(self.layer['app'])
        self.error_setup()

    def error_setup(self):
        """ """
        self.browser.handleErrors = False
        self.portal.error_log._ignored_exceptions = ()

        def raising(self, info):
            import traceback
            traceback.print_tb(info[2])
            print (info[1])

        from Products.SiteErrorLog.SiteErrorLog import SiteErrorLog
        SiteErrorLog.raising = raising

    def login_as_admin(self):
        """ Perform through-the-web login."""

        # Go admin
        browser = self.browser
        browser.open(self.portal_url + '/login_form')
        browser.getControl(name='__ac_name').value = SITE_OWNER_NAME
        browser.getControl(name='__ac_password').value = SITE_OWNER_PASSWORD
        browser.getControl(name='submit').click()

    def test_widget(self):
        """" """
        self.login_as_admin()

        with open(os.path.join(FHIR_FIXTURE_PATH, 'Organization.json'), 'r') as f:
            json_object_str = f.read()

        browser = self.browser
        browser.open(self.portal_url + '/++add++TestToken')
        # ** CONTROLS
        # for x in browser.getForm(index=1).mech_form.controls: print  x.name
        # form.widgets.IBasic.title
        # form.widgets.IBasic.description
        # form.widgets.IDublinCore.title
        # form.widgets.IDublinCore.description
        # form.widgets.resource
        # form.widgets.IDublinCore.subjects
        # form.widgets.IDublinCore.language:list
        # form.widgets.IDublinCore.language-empty-marker
        # form.widgets.IDublinCore.effective-day
        # form.widgets.IDublinCore.effective-month
        # form.widgets.IDublinCore.effective-year
        # form.widgets.IDublinCore.effective-calendar
        # form.widgets.IDublinCore.effective-hour
        # form.widgets.IDublinCore.effective-minute
        # form.widgets.IDublinCore.effective-timezone
        # form.widgets.IDublinCore.effective-empty-marker
        # form.widgets.IDublinCore.expires-day
        # form.widgets.IDublinCore.expires-month
        # form.widgets.IDublinCore.expires-year
        # form.widgets.IDublinCore.expires-calendar
        # form.widgets.IDublinCore.expires-hour
        # form.widgets.IDublinCore.expires-minute
        # form.widgets.IDublinCore.expires-timezone
        # form.widgets.IDublinCore.expires-empty-marker
        # form.widgets.IDublinCore.creators
        # form.widgets.IDublinCore.contributors
        # form.widgets.IDublinCore.rights
        # form.buttons.save
        # form.buttons.cancel
        browser.getControl(name='form.widgets.IBasic.title').value = 'hello organization'
        browser.getControl(name='form.widgets.resource').value = json_object_str
        browser.getControl(name='form.buttons.save').click()
        # There must be form error! as required title is missing so url is unchanged
        self.assertEqual(browser.mech_browser.geturl(), self.portal_url + '/++add++TestToken')
        # Test Value exist, even form resubmit
        self.assertEqual(
            json.loads(browser.getControl(name='form.widgets.resource').value),
            json.loads(json_object_str))

        # Let's fullfill required
        browser.getControl(name='form.widgets.IDublinCore.title').value = 'hello organization'
        # After solving that problem, this again value assign not need
        browser.getControl(name='form.widgets.resource').value = json_object_str
        browser.getControl(name='form.buttons.save').click()
        # should suceess now and redirect to view page
        self.assertEqual(browser.mech_browser.geturl(), 'http://localhost:55001/plone/testtoken/view')

        # let's try edit
        browser.open('http://localhost:55001/plone/testtoken/edit')
        json_object_str = browser.getControl(name='form.widgets.resource').value

        json_object = json.loads(json_object_str)
        json_object['text']['div'] = '<div>modified</div>'
        browser.getControl(name='form.widgets.resource').value = json.dumps(json_object)
        browser.getControl(name='form.buttons.save').click()
        # should sucess
        self.assertIn('class="portalMessage info"', browser.contents)
        self.assertIn('Changes saved', browser.contents)
        self.assertEqual(browser.mech_browser.geturl(), 'http://localhost:55001/plone/testtoken')
