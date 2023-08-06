from django.db import models

from price_level.models import Pricable


class PricableModel(Pricable, models.Model):
    pass
