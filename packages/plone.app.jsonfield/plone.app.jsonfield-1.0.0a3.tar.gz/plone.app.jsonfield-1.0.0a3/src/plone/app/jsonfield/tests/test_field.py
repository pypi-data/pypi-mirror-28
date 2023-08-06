# _*_ coding: utf-8 _*_
from . import FHIR_FIXTURE_PATH
from plone.app.jsonfield import field
from plone.app.jsonfield.interfaces import IJSONValue
from zope.interface import Invalid
from zope.schema.interfaces import WrongType

import json
import os
import six
import unittest


__author__ = 'Md Nazrul Islam<email2nazrul@gmail.com>'


class FieldIntegrationTest(unittest.TestCase):
    """ """

    def test_init_validate(self):  # noqa: C901
        """ """
        # Test with minimal params
        try:
            field.JSON(
                title=six.text_type('Organization resource'),
            )
        except Invalid as exc:
            raise AssertionError('Code should not come here, as everything should goes fine.\n{0!s}'.format(exc))

        with open(os.path.join(FHIR_FIXTURE_PATH, 'Organization.schema.json'), 'r') as f:
            json_object_schema = json.load(f)

        try:
            field.JSON(
                title=six.text_type('Organization resource'),
                json_schema=json_object_schema
            )
        except Invalid as exc:
            raise AssertionError('Code should not come here, as everything should goes fine.\n{0!s}'.format(exc))

        try:
            field.JSON(
                title=six.text_type('Organization resource'),
                json_schema=[1, 2]
            )
            raise AssertionError('Code should not come here, because invalid format json schema is provided')
        except WrongType:
            pass

        try:
            field.JSON(
                title=six.text_type('Organization resource'),
                json_schema=field
            )
            raise AssertionError('Code should not come here, because invalid format json schema is provided')
        except Invalid as exc:
            self.assertIn('Invalid schema data type', str(exc))

    def test_from_iterable(self):
        """ """
        with open(os.path.join(FHIR_FIXTURE_PATH, 'Organization.json'), 'r') as f:
            json_object_iter = json.load(f)

        with open(os.path.join(FHIR_FIXTURE_PATH, 'Organization.schema.json'), 'r') as f:
            json_object_schema = json.load(f)

        fhir_field = field.JSON(
            title=six.text_type('Organization resource'),
            json_schema=json_object_schema
        )

        try:
            fhir_resource_value = fhir_field.from_iterable(json_object_iter)
        except Invalid as exc:
            raise AssertionError(
                'Code should not come here! as should return valid JSONValue.\n{0!s}'.format(exc)
                )

        self.assertEqual(fhir_resource_value['resourceType'], json_object_iter['resourceType'])

        with open(os.path.join(FHIR_FIXTURE_PATH, 'Products.array.json'), 'r') as f:
            json_array_iter = json.load(f)

        fhir_field.json_schema = None
        try:
            fhir_resource_value = fhir_field.from_iterable(json_array_iter)
        except Invalid as exc:
            raise AssertionError(
                'Code should not come here! as should return valid JSONValue.\n{0!s}'.format(exc)
                )
        self.assertTrue(IJSONValue.providedBy(fhir_resource_value))

    def test_fromUnicode(self):
        """ """

        with open(os.path.join(FHIR_FIXTURE_PATH, 'Organization.schema.json'), 'r') as f:
            json_object_schema = json.load(f)

        with open(os.path.join(FHIR_FIXTURE_PATH, 'Organization.json'), 'r') as f:
            json_str = f.read()

        fhir_field = field.JSON(
            title=six.text_type('Organization resource'),
            json_schema=json_object_schema
        )

        try:
            fhir_resource_value = fhir_field.fromUnicode(json_str)
        except Invalid as exc:
            raise AssertionError(
                'Code should not come here! as should return valid JSONValue.\n{0!s}'.format(exc)
                )
        self.assertTrue(IJSONValue.providedBy(fhir_resource_value))
        # Test with invalid json string
        try:
            invalid_data = '{hekk: invalg, 2:3}'
            fhir_field.fromUnicode(invalid_data)
            raise AssertionError('Code should not come here! invalid json string is provided')
        except Invalid as exc:
            self.assertIn('Invalid JSON String', str(exc))

    def test_fromUnicodewith_empty_string(self):
        """ """
        fhir_field = field.JSON(
            title=six.text_type('Organization resource'),
            required=False
        )
        value = fhir_field.fromUnicode('')
        self.assertIsNone(value)

    def test_field(self):
        """ """
        with open(os.path.join(FHIR_FIXTURE_PATH, 'Organization.schema.json'), 'r') as f:
            json_object_schema = json.load(f)

        with open(os.path.join(FHIR_FIXTURE_PATH, 'Organization.json'), 'r') as f:
            json_object_iter = json.load(f)

        fhir_field1 = field.JSON(
            title=six.text_type('Organization resource'),
            json_schema=json_object_schema,
            default=json_object_iter
        )

        with open(os.path.join(FHIR_FIXTURE_PATH, 'Organization.json'), 'r') as f:
            json_object_str = f.read()

        fhir_field2 = field.JSON(
            title=six.text_type('Organization resource'),
            json_schema=json_object_schema,
            default=json_object_str
        )

        self.assertEqual(fhir_field1.default, fhir_field2.default)
