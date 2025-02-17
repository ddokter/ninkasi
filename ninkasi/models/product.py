from django.db import models
from django.utils.translation import gettext_lazy as _


class Product(models.Model):

    """Final product that the brewery turns out. This is the end
    product of a batch and may be stuff like kegs, bottles, etc.  It
    is linked to materials, so a deliverable could be N boxes of
    bottles, that are linked to both a box and N bottles.

    """

    name = models.CharField(max_length=50)
    volume = models.FloatField()
    unit = models.ForeignKey("Unit", on_delete=models.CASCADE)
    material = models.ManyToManyField(
        "Material", through="ProductMaterial", blank=True, null=True)

    def __str__(self):

        return self.name

    def get_liter_volume(self):

        """ Return the volume in liters """

        return self.unit.convert(self.volume, "Liter")

    def list_productmaterials(self):

        """ Products consist of one or more materials. """

        return self.productmaterial_set.all()

    class Meta:

        app_label = "ninkasi"
        ordering = ["name"]


class ProductMaterial(models.Model):

    """ Coupling of product to separate materials """

    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    material = models.ForeignKey("Material", on_delete=models.CASCADE)
    amount = models.FloatField()

    def __str__(self):

        return f"{ self.product } { self.material } * { self.amount }"
