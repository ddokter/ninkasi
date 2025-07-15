from django.db import models
from .ingredient import Ingredient
from .fields import FloatRangeField


class MaltBase(Ingredient):

    color = FloatRangeField()
    proteine = FloatRangeField()
    moisture = FloatRangeField()

    class Meta:
        abstract = True


class Malt(MaltBase):

    """Malt types. Should define the malts that are available in an
    abstract sense. Most software systems use specific brands as
    ingredients, but Ninkasi doesn't.

    """

    def list_products(self):

        return self.maltproduct_set.all()

    class Meta:
        app_label = "ninkasi"
        ordering = ["name"]


class MaltProduct(MaltBase):

    """Specific product of a malt family. This is defined by a brand,
    but not the same as an actual batch of that product. The latter is
    only defined for inventory items or brews.

    """

    base = models.ForeignKey("Malt", on_delete=models.CASCADE)
    brand = models.ForeignKey("Brand", on_delete=models.CASCADE)

    def __str__(self):

        return f"{self.brand} {self.name}"

    @property
    def substitutes(self):

        """ Return any siblings """

        return self.base.maltproduct_set.exclude(id=self.id)

    class Meta:
        app_label = "ninkasi"
        ordering = ["name"]


class MaltMap(models.Model):

    """ Map imported malt to Ninkasi malt """

    from_malt = models.CharField(max_length=100)
    to_malt = models.ForeignKey("Malt", on_delete=models.CASCADE)
