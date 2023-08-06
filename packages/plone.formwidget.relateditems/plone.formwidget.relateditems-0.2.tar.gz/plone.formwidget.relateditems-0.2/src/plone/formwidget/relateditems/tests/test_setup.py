# -*- coding: utf-8 -*-
"""Test Setup of plone.formwidget.relateditems."""

from plone import api
from plone.browserlayer.utils import registered_layers
from plone.formwidget.relateditems import config
from plone.formwidget.relateditems.testing import INTEGRATION_TESTING

import unittest


class TestSetup(unittest.TestCase):
    """Validate setup process for plone.formwidget.relateditems."""

    layer = INTEGRATION_TESTING

    def setUp(self):
        """Custom shared utility setup for tests."""
        self.portal = self.layer['portal']
        self.installer = api.portal.get_tool('portal_quickinstaller')

    def test_product_installed(self):
        """Validate that our product is installed."""
        self.assertTrue(
            self.installer.isProductInstalled(config.PROJECT_NAME),
        )

    def test_addon_layer(self):
        """Validate that the browserlayer for our product is installed."""
        layers = [l.getName() for l in registered_layers()]
        self.assertIn('IPloneFormwidgetRelateditemsLayer', layers)


class TestUninstall(unittest.TestCase):
    """Validate uninstall process for plone.formwidget.relateditems."""

    layer = INTEGRATION_TESTING

    def setUp(self):
        """Custom shared utility setup for tests."""
        self.portal = self.layer['portal']
        self.installer = api.portal.get_tool('portal_quickinstaller')
        self.installer.uninstallProducts([config.PROJECT_NAME])

    def test_product_uninstalled(self):
        """Validate that our product is uninstalled."""
        self.assertFalse(self.installer.isProductInstalled(
            config.PROJECT_NAME,
        ))

    def test_addon_layer_removed(self):
        """Validate that the browserlayer is removed."""
        layers = [l.getName() for l in registered_layers()]
        self.assertNotIn('IPloneFormwidgetRelateditemsLayer', layers)
