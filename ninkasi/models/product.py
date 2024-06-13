from django.db import models
from django.utils.translation import gettext_lazy as _


CONVERSION_TABLE = {
    'cl': 0.01,
    'ml': 0.001,
    'l': 1
}


class Product(models.Model):

    """Final product that the brewery turns out. This is the end
    product of a batch and may be stuff like kegs, bottles, etc.

    """

    name = models.CharField(max_length=50)
    volume = models.SmallIntegerField()
    unit = models.ForeignKey("Unit", on_delete=models.CASCADE)

    def __str__(self):

        return self.name

    def get_liter_volume(self):

        """ Return the volume in liters """

        # TODO: this should really be part of the unit

        return self.volume * CONVERSION_TABLE[self.unit.abbreviation.lower()]

    class Meta:

        app_label = "ninkasi"
        ordering = ["name"]
