from django.db import models
from django.utils.translation import gettext_lazy as _


class Material(models.Model):

    """ Anything needed for a batch. Can be an ingredient, but also bottles
    or labels.  """

    name = models.CharField(_("Name"), max_length=100)
    description = models.TextField(_("Description"), null=True, blank=True)
    category = models.ManyToManyField("Category", blank=True)

    def __str__(self):

        return self.name

    @property
    def list_categories(self):

        return self.category.all()

    class Meta:
        app_label = "ninkasi"
        ordering = ["name"]


class ParentedMaterial(models.Model):

    """Materials may be related to a brew or batch. Define base
    properties.

    """

    amount = models.FloatField(_("Amount"))
    unit = models.ForeignKey("Unit", on_delete=models.CASCADE)
    material = models.ForeignKey(Material, on_delete=models.CASCADE)
    brand = models.CharField(null=True, blank=True, max_length=100)
    batchnr = models.CharField(_("Batch Nr"), max_length=100)

    def __str__(self):

        return f"{ self.material } { self.brand } { self.amount }"

    class Meta:
        abstract = True
