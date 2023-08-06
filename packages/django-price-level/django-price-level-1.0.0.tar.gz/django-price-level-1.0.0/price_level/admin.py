from django.contrib import admin

from . import models


@admin.register(models.PriceLevel)
class PriceLevelAdmin(admin.ModelAdmin):
    """Admin model for PriceLevels."""

    list_display = ('name', 'pricable', 'price', 'category', 'takes_effect_on')
    list_filter = ('pricable', 'category')
