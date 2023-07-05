from django.db import models
from django.utils.translation import gettext_lazy as _


class Phase(models.Model):

    """ Phases in the production process, from brewing until sale.
    The phases are meant as markers for measurements, so 'end of boil'
    is as valid a phase as boil itself.
    """

    name = models.CharField(_("Name"), unique=True, max_length=100)

    def __str__(self):

        return self.name

    class Meta:

        app_label = "ninkasi"
        ordering = ["name"]
        verbose_name_plural = _("Phases")
