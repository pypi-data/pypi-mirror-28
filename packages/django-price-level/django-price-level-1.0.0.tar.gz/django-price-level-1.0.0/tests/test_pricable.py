#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
test_django-price-level
------------

Tests for `Pricable` models module.
"""
import datetime

from django.test import TestCase

from model_mommy import mommy


class TestDjango_price_level(TestCase):

    def test_get_current_price_level(self):
        price_level = mommy.make(
            "PriceLevel",
            name="Foo price level",
            takes_effect_on=datetime.date(year=2017, month=1, day=1),
        )
        result = price_level.pricable.get_current_price_level(date_time=datetime.date(year=2017, month=1, day=1))
        self.assertEqual(result, price_level)

    def test_get_current_price_level_none(self):
        price_level = mommy.make(
            "PriceLevel",
            name="Foo price level",
            takes_effect_on=datetime.date(year=2017, month=1, day=2),
        )
        result = price_level.pricable.get_current_price_level(date_time=datetime.date(year=2017, month=1, day=1))
        self.assertEqual(result, None)
