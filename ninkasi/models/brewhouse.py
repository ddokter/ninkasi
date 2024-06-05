from django.db import models
from django.utils.translation import gettext_lazy as _
from .container import Container
from .fields import DurationField


WARMUP_HELP = _("Time in minutes needed for 1 degree C warmup.")

NEXT_HELP = _("Minimal time needed before the next brew can be started.")

FILTER_LOSS = _("Amount of wordt lost in filter dead space.")

WHIRLPOOL_LOSS = _("Amount of wordt lost in whirlpool dead space.")


class Brewhouse(Container):

    """Represent brewing installation. This defines a few parameters
    for the machinery as well, that may be effecting quality.

    """

    warmup = models.SmallIntegerField(_("Warmup time per degree C"),
                                      help_text=WARMUP_HELP)
    next_brew_delay = DurationField(_("Minimal brewtime before next brew"),
                                    help_text=NEXT_HELP)
    filter_loss = models.SmallIntegerField(_("Amount lost in filter"),
                                           help_text=FILTER_LOSS)
    spent_grain_loss = models.SmallIntegerField(_("Spent grain loss per Kg"))
    whirlpool_loss = models.SmallIntegerField(_("Amount lost in whirlpool"),
                                              help_text=WHIRLPOOL_LOSS)

    def __str__(self):

        return f"{ self.name } { self.volume }L"

    def content(self, date):

        """ Is the installation available on this day? """

        return self.brew_set.filter(date__date=date).first()

    def total_loss(self, recipe):

        """ Return the total losses for this machinery, given a recipe """

        return (recipe.get_grist_weigth() * self.spent_grain_loss +
                self.filter_loss + self.whirlpool_loss)

    class Meta:

        app_label = "ninkasi"
        ordering = ["name"]
        verbose_name_plural = _("Brewhouses")
