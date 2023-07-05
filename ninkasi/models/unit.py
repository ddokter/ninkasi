from django.db import models
from django.utils.translation import gettext_lazy as _


class Unit(models.Model):

    name = models.CharField(_("Name"), max_length=100)

    def __str__(self):

        return self.name

    class Meta:

        app_label = "ninkasi"
        ordering = ["name"]
        verbose_name_plural = _("Units")
