#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
test_django-price-level
------------

Tests for `PriceLevel` models module.
"""

from django.test import TestCase

from price_level import models


class TestDjango_price_level(TestCase):

    def test_str(self):
        price_level = models.PriceLevel(name="Foo price level")
        self.assertEqual(str(price_level), "Foo price level")
