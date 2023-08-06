# -*- coding: utf-8 -*-
"""Tests for plone.formwidget.relateditems.widget."""

from mock import Mock
from zope.publisher.browser import TestRequest

import unittest


class RelatedItemsWidgetTests(unittest.TestCase):

    def setUp(self):
        self.request = TestRequest(environ={'HTTP_ACCEPT_LANGUAGE': 'en'})

    def test_fieldwidget(self):
        from plone.formwidget.relateditems.widget import RelatedItemsWidget
        from plone.formwidget.relateditems.widget import RelatedItemsFieldWidget
        field = Mock(__name__='field', title=u'', required=True)
        vocabulary = Mock()
        request = Mock()
        widget = RelatedItemsFieldWidget(field, vocabulary, request)
        self.assertTrue(isinstance(widget, RelatedItemsWidget))
        self.assertIs(widget.field, field)
        self.assertIs(widget.request, request)
