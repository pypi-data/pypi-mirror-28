# _*_ coding: utf-8 _*_
from . import FHIR_FIXTURE_PATH
from plone.app.jsonfield import value
from plone.app.jsonfield.compat import NO_VALUE
from plone.app.jsonfield.interfaces import IJSONValue
from zope.interface import Invalid
from zope.schema.interfaces import WrongType

import datetime
import json
import os
import six
import unittest


__author__ = 'Md Nazrul Islam<email2nazrul@gmail.com>'


class ValueIntegrationTest(unittest.TestCase):
    """ """
    def test_json_value(self):
        """ """
        with open(os.path.join(FHIR_FIXTURE_PATH, 'Organization.json'), 'r') as f:
            json_object_iter = json.load(f)

        with open(os.path.join(FHIR_FIXTURE_PATH, 'Organization.schema.json'), 'r') as f:
            json_object_schema = json.load(f)

        json_object_value = value.JSONObjectValue(json_object_iter, schema=json_object_schema)

        self.assertTrue(IJSONValue.providedBy(json_object_value))
        self.assertEqual(json_object_iter.keys(), json_object_value.keys())

        with open(os.path.join(FHIR_FIXTURE_PATH, 'Products.array.json'), 'r') as f:
            json_array_iter = json.load(f)

        with open(os.path.join(FHIR_FIXTURE_PATH, 'Products.array.schema.json'), 'r') as f:
            json_array_schema = json.load(f)

        json_array_value = value.JSONArrayValue(json_array_iter, schema=json_array_schema)
        self.assertTrue(IJSONValue.providedBy(json_array_value))

        json_object_value_empty = value.JSONObjectValue(NO_VALUE)
        json_array_value_empty = value.JSONArrayValue(NO_VALUE)

        self.assertTrue(IJSONValue.providedBy(json_object_value_empty))
        self.assertEqual(0, len(json_object_value_empty))
        self.assertTrue(IJSONValue.providedBy(json_array_value_empty))
        self.assertEqual(0, len(json_array_value_empty))

        # TEST: stringify
        self.assertIsInstance(json_object_value.stringify(), six.string_types)
        self.assertEqual(len(json_object_value.stringify()), len(json.dumps(json_object_iter)))
        self.assertEqual(json_array_value.stringify(), json.dumps(json_array_iter))
        # json indent, prettification, should be new line exists
        self.assertNotIn('\\n', json_object_value.stringify(True))

        self.assertEqual(json_object_value_empty.stringify(), '{}')  # noqa: P103
        self.assertEqual(json_array_value_empty.stringify(), '[]')

        # TEST: patch
        patch_data = [
            {'path': '/text/status', 'value': 'patched!', 'op': 'replace'}
        ]
        json_object_value.patch(patch_data)
        self.assertEqual('patched!', json_object_value['text']['status'])

        # Empty Object can't be patcahed!
        try:
            json_object_value_empty.patch(patch_data)
            raise AssertionError('Code should not come here! because member `text` should not found in empty object')
        except Invalid as exc:
            self.assertIn('member \'text\' not found in {}', str(exc))  # noqa: P103

        # Array is not patchable
        try:
            json_array_value.patch(patch_data)
            raise AssertionError(
                'Code should not come here! because array data is not patchable!'
            )
        except Invalid as exc:
            self.assertEqual('json patch is not applicable on array type value!', str(exc))

        # wrong patch format!
        patch_data = {'hello': 123}
        try:
            json_object_value.patch(patch_data)
            raise AssertionError('Code should not come here! because wrong type data is provided for patch!')
        except WrongType:
            pass
        # wrong path!
        patch_data = [
            {'path': '/text/fake path', 'value': 'patched!', 'Invalid Option': 'replace'}
        ]
        # Test getting original error from json patcher
        try:
            json_object_value.patch(patch_data)
            raise AssertionError(
                'Code should not come here! because wrong patch data is provided for patch and invalid format as well!'
            )
        except Invalid as exc:
            self.assertIn("does not contain 'op' member", str(exc))

    def test_validation(self):
        """" """
        with open(os.path.join(FHIR_FIXTURE_PATH, 'Organization.schema.json'), 'r') as f:
            json_object_schema = json.load(f)

        with open(os.path.join(FHIR_FIXTURE_PATH, 'Products.array.schema.json'), 'r') as f:
            json_array_schema = json.load(f)

        json_object_iter = {'hello': 'ketty'}
        json_array_iter = [{'hello': 'ketty'}, 99, True]

        json_object_value = value.JSONObjectValue(json_object_iter)
        json_array_value = value.JSONArrayValue(json_array_iter)

        # TEST: schema contraint
        try:
            json_object_value._validate_object(json_object_iter, schema=json_object_schema)
            raise AssertionError('Code should not come here! because error should come from jsonschema')
        except Invalid as exc:
            self.assertIn('Failed validating', str(exc))

        try:
            json_array_value._validate_object(json_array_iter, schema=json_array_schema)
            raise AssertionError('Code should not come here! because error should come jsonschema')
        except Invalid as exc:
            self.assertIn('Failed validating', str(exc))

        try:
            json_object_value._validate_object(datetime.datetime.now())
            raise AssertionError('Code should not come here! because error should come jsonschema')
        except Invalid as exc:
            self.assertIn('Only dict or list type', str(exc))

        try:
            json_object_value._validate_object(json_array_value)
            raise AssertionError('Code should not come here! because wrong data type list is provided')
        except Invalid as exc:
            self.assertIn('given value must be dict type', str(exc))

        try:
            json_array_value._validate_object(json_object_value)
            raise AssertionError('Code should not come here! because wrong data type dict is provided')
        except Invalid as exc:
            self.assertIn('given value must be array type', str(exc))

        try:
            json_array_value._validate_object('wrong type')
            raise AssertionError('Code should not come here! because wrong data type is provided')
        except WrongType as exc:
            self.assertEqual('value must be json serialable!', str(exc))
