from django.db import models
from django.utils.translation import gettext_lazy as _


class Product(models.Model):

    """Final product that the brewery turns out. This is the end
    product of a batch and may be stuff like kegs, bottles, etc.

    """

    name = models.CharField(max_length=50)
    volume = models.FloatField()
    unit = models.ForeignKey("Unit", on_delete=models.CASCADE)

    def __str__(self):

        return self.name

    def get_liter_volume(self):

        """ Return the volume in liters """

        return self.unit.convert(self.volume, "Liter")

    class Meta:

        app_label = "ninkasi"
        ordering = ["name"]
