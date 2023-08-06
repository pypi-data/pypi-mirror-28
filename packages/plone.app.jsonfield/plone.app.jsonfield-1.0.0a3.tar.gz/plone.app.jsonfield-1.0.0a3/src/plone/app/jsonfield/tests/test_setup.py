# -*- coding: utf-8 -*-
"""Setup tests for this package."""
from plone import api
from plone.app.jsonfield.testing import PLONE_APP_JSON_FIELD_INTEGRATION_TESTING  # noqa
from Products.CMFPlone.interfaces import INonInstallable
from zope.component import queryUtility

import unittest


class TestSetup(unittest.TestCase):
    """Test that plone.app.jsonfield is properly installed."""

    layer = PLONE_APP_JSON_FIELD_INTEGRATION_TESTING

    def setUp(self):
        """Custom shared utility setup for tests."""
        self.portal = self.layer['portal']
        self.installer = api.portal.get_tool('portal_quickinstaller')

    def test_product_installed(self):
        """Test if plone.app.jsonfield is installed."""
        self.assertTrue(self.installer.isProductInstalled(
            'plone.app.jsonfield'))


class TestUninstall(unittest.TestCase):

    layer = PLONE_APP_JSON_FIELD_INTEGRATION_TESTING

    def setUp(self):
        self.portal = self.layer['portal']
        self.installer = api.portal.get_tool('portal_quickinstaller')
        self.installer.uninstallProducts(['plone.app.jsonfield'])

    def test_product_uninstalled(self):
        """Test if plone.app.jsonfield is cleanly uninstalled."""
        self.assertFalse(self.installer.isProductInstalled(
            'plone.app.jsonfield'))

    def test_hidden_profiled(self):
        """Test if plone.app.jsonfield hidden profile utility is available"""

        utility = queryUtility(INonInstallable, name='plone.app.jsonfield-hiddenprofiles')

        self.assertIsNotNone(utility)
        self.assertIn('plone.app.jsonfield:uninstall', utility.getNonInstallableProfiles())
