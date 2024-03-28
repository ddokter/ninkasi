from django.db import models
from django.utils.translation import gettext_lazy as _
from .container import Container


WARMUP_HELP = _("Time in minutes needed for 1 degree C warmup")


class Brewhouse(Container):

    """Represent brewing installation. This defines a few parameters
    for the installation as well, that may be effecting quality.

    """

    warmup = models.SmallIntegerField(_("Warmup time per degree C"),
                                      help_text=WARMUP_HELP,
                                      blank=True, null=True)


    def __str__(self):

        return f"{ self.name } { self.volume }L"

    def content(self, date):

        """ Is the installation available on this day? """

        return self.brew_set.filter(date__date=date).first()

    class Meta:

        app_label = "ninkasi"
        ordering = ["name"]
        verbose_name_plural = _("Brewhouses")
