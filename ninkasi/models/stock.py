from django.db import models
from django.utils.translation import gettext_lazy as _


class Stock(models.Model):

    """Final product that the brewery turns out. This is the end
    product of a batch and may be stuff like kegs, bottles, etc.  It
    is linked to materials, so a deliverable could be N boxes of
    bottles, that are linked to both a box and N bottles.

    """

    amount = models.FloatField()
    unit = models.ForeignKey("Unit", on_delete=models.CASCADE)
    material = models.ForeignKey("Material", on_delete=models.CASCADE)
    brand = models.ForeignKey("Brand", on_delete=models.CASCADE)
    batchnr = models.CharField(_("Batch Nr"), max_length=100,
                               null=True, blank=True)

    def __str__(self):

        return f"{self.material} ({self.brand}) {self.amount}{self.unit}"

    class Meta:

        app_label = "ninkasi"
        ordering = ["material__name"]
