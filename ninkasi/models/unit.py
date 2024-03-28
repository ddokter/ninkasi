from django.db import models
from django.utils.translation import gettext_lazy as _


class Unit(models.Model):

    """ Represent units in the system, for weight, volume, etc. """

    name = models.CharField(_("Name"), max_length=100)
    abbreviation = models.CharField(_("Abbreviation"), max_length=50,
                                    null=True, blank=True)

    def __str__(self):

        return self.abbreviation or self.name

    class Meta:

        app_label = "ninkasi"
        ordering = ["name"]
        verbose_name_plural = _("Units")
