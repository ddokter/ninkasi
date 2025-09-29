from django.db import models
from django.utils.translation import gettext_lazy as _
from .ingredient import Ingredient
from .fields import FloatRangeField
from ninkasi.resource import ResourceRegistry


HOP_FORM_VOCAB = [(0, _("Flower")),
                  (1, _("Pellet T90")),
                  (2, _("Pellet Cryo"))]


class Hop(Ingredient):

    """Hop class, defining the family of hop and the ranges of
    essential features like alpha acid. The Hop family is typically
    used in recipes, where the actual product may be used for a given
    brew or batch.

    """

    alpha_acid = FloatRangeField()
    beta_acid = FloatRangeField(null=True, blank=True)
    substitutes = models.ManyToManyField("Hop", null=True, blank=True)

    class Meta:
        app_label = "ninkasi"
        ordering = ["name"]


class HopProduct(Ingredient):

    """Specific product of a hop family. This is defined by a brand,
    but not the same as an actual batch of that product."""

    base = models.ForeignKey("Hop", on_delete=models.CASCADE)
    brand = models.ForeignKey("Brand", on_delete=models.CASCADE)
    form = models.SmallIntegerField(choices=HOP_FORM_VOCAB)

    class Meta:
        app_label = "ninkasi"
        ordering = ["name"]
