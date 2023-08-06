# _*_ coding: utf-8 _*_
from . import FHIR_FIXTURE_PATH
from plone.app.jsonfield import compat
from plone.app.jsonfield import helpers
from plone.app.jsonfield.testing import PLONE_APP_JSON_FIELD_INTEGRATION_TESTING
from zope.interface import Invalid

import os
import unittest


__author__ = 'Md Nazrul Islam<email2nazrul@gmail.com>'


class HelperIntegrationTest(unittest.TestCase):
    """ """
    layer = PLONE_APP_JSON_FIELD_INTEGRATION_TESTING

    def test_parse_json_str(self):
        """ """
        with open(os.path.join(FHIR_FIXTURE_PATH, 'Organization.json'), 'r') as f:
            json_str = f.read()

        dict_data = helpers.parse_json_str(json_str)

        self.assertEqual(dict_data['resourceType'], 'Organization')

        json_str = """
        {"resourceType": "Task", Wrong: null}
        """
        try:
            helpers.parse_json_str(json_str)
            raise AssertionError('Code shouldn\'t come here! as invalid json string is provided')
        except Invalid:
            pass

    def test_parse_json_str_with_empty(self):
        """ """
        value = helpers.parse_json_str(compat.NO_VALUE)
        self.assertIsNone(value)

        value = helpers.parse_json_str(compat.EMPTY_STRING)
        self.assertIsNone(value)

        value = helpers.parse_json_str(None)
        self.assertIsNone(value)
