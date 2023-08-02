from django.db import models
from django.utils.translation import gettext_lazy as _
from .brew import Brew


class Brewhouse(models.Model):

    """ Represent brewing installation
    """

    name = models.CharField(_("Name"), null=True, blank=True, max_length=100)
    volume = models.SmallIntegerField(_("Volume"))


    def __str__(self):

        return f"{ self.name } { self.volume }L"

    def content(self, date):

        """ Is this tank full or empty on this day """

        return self.brew_set.filter(date__date=date).first()
        
    class Meta:

        app_label = "ninkasi"
        ordering = ["name"]
        verbose_name_plural = _("Brewhouses")
