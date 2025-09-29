from django.db import models
from django.utils.translation import gettext_lazy as _
from .ingredient import Ingredient
from .fields import FloatRangeField
from ninkasi.resource import ResourceRegistry


class Other(Ingredient):

    """Misc ingredient

    """

    class Meta:
        app_label = "ninkasi"
        ordering = ["name"]


class OtherProduct(Ingredient):

    """Specific product. This is defined by a brand,
    but not the same as an actual batch of that product."""

    base = models.ForeignKey("Other", on_delete=models.CASCADE)
    brand = models.ForeignKey("Brand", on_delete=models.CASCADE)

    class Meta:
        app_label = "ninkasi"
        ordering = ["name"]
