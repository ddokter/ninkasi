from django.db import models
from django.utils.translation import gettext_lazy as _
from django.contrib.contenttypes.fields import GenericForeignKey
from django.contrib.contenttypes.models import ContentType
from django.conf import settings


class BasePhase:

    """Base class for defining phases. Extend this class for
    implementing any type of phase.

    """

    def get_duration(self):

        """ Return total of all steps """

        return sum(step.get_total_duration() for step in self.list_steps())

    def list_steps(self):

        """ Return list of all steps for this phase """


class Phase(models.Model, BasePhase):

    """Phases in the production process, relevant to the lifecycle of
    a batch or brew. This could be anything, from 'boil' to
    'maturation'. Defintion of phases is part of the system setup and
    up to the brewer. However, usually the phases will reflect the
    standard process of: grind, mash, filter, boil, whirlpool, chill,
    ferment and mature. The phase is defined upon the batch, brew but
    also recipe.

    """

    name = models.CharField(_("Name"), unique=True, max_length=100)
    definition = models.TextField(_("Definition"))

    def __str__(self):

        return self.name

    class Meta:

        app_label = "ninkasi"
        ordering = ["name"]
        verbose_name_plural = _("Phases")


class BatchPhase(models.Model, BasePhase):

    """Batch related phase. The subphases of a batch are timed, more
    than defined by a duration.

    """

    phase = models.ForeignKey("Phase", on_delete=models.PROTECT)
    batch = models.ForeignKey("Batch", on_delete=models.CASCADE)

    def __str__(self):

        return self.phase.name

    def list_steps(self):

        """ Get the batch steps """

        return self.batchstep_set.all()

    class Meta:

        app_label = "ninkasi"
        ordering = ["phase__name"]
        verbose_name_plural = _("Phases")


class RecipePhase(models.Model, BasePhase):

    """Recipe related phase.

    """

    phase = models.ForeignKey("Phase", on_delete=models.PROTECT)
    recipe = models.ForeignKey(settings.RECIPE_MODEL, on_delete=models.CASCADE)

    def __str__(self):

        return self.phase.name

    def list_steps(self):

        """ Get the batch steps """

        return self.recipestep_set.all()

    class Meta:

        app_label = "ninkasi"
        ordering = ["phase__name"]
        verbose_name_plural = _("Phases")
