from django.db import models
from django.utils.translation import gettext_lazy as _


class Quantity(models.Model):

    """Things that can be measured in Ninkasi. This is stuff like
    volume, acidity, FAN, etc. A quantity should also specify a list
    of units that may be used to express a measurement.

    """

    name = models.CharField(max_length=50)
    units = models.ManyToManyField("Unit", blank=True, null=True)

    def __str__(self):

        return self.name

    class Meta:

        app_label = "ninkasi"
        ordering = ["name"]
        verbose_name_plural = _("Quantities")
