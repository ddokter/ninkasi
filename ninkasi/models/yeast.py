from django.db import models
from django.utils.translation import gettext_lazy as _
from .ingredient import Ingredient
from .fields import FloatRangeField, IntRangeField


YEAST_FORM_VOCAB = [(0, _("Dry")),
                    (1, _("Liquid")),
                    (2, _("Slurry"))]

FLOC_VOCAB = ((0, _('Low')), (1, _('Medium')), (2, _('High')))


class YeastBase(Ingredient):

    attenuation = IntRangeField()
    flocculation = models.SmallIntegerField(choices=FLOC_VOCAB)

    class Meta:
        abstract = True


class Yeast(YeastBase):

    """Yeast class, defining the family of yeast and the ranges of
    essential features like alpha acid. The Yeast family is typically
    used in recipes, where the actual product may be used for a given
    brew or batch.

    """

    class Meta:
        app_label = "ninkasi"
        ordering = ["name"]


class YeastProduct(YeastBase):

    """Specific product of a yeast family. This is defined by a brand,
    but not the same as an actual batch of that product. However, the
    yeast does not _need_ to have a parent. Many products have unknown
    origins.

    """

    base = models.ForeignKey("Yeast", on_delete=models.CASCADE,
                             blank=True, null=True)
    brand = models.ForeignKey("Brand", on_delete=models.CASCADE)
    form = models.SmallIntegerField(choices=YEAST_FORM_VOCAB)

    class Meta:
        app_label = "ninkasi"
        ordering = ["name"]
