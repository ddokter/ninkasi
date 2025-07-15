from django.db import models
from django.utils.translation import gettext_lazy as _


class InventoryItem(models.Model):

    """Define inventory for the brewery. An inventory item
    essentially is an amount of materials that is in store.

    """

    amount = models.FloatField()
    unit = models.ForeignKey("Unit", on_delete=models.CASCADE)
    material = models.ForeignKey("Material", on_delete=models.CASCADE)
    brand = models.ForeignKey("Brand", on_delete=models.CASCADE,
                              null=True, blank=True
                              )
    batchnr = models.CharField(_("Batch Nr"), max_length=100)

    def __str__(self):

        if self.brand:
            return f"{self.material} ({self.brand}) {self.amount}{self.unit}"
        else:
            return f"{self.material} {self.amount}{self.unit}"

    class Meta:

        app_label = "ninkasi"
        ordering = ["material__name"]
