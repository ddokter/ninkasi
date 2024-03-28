from django.db import models
from django.utils.translation import gettext_lazy as _
from .phase import Phase
from .fields import DurationField


DURATION_VOCAB = [
    (0, _("Minute")),
    (1, _("Hour")),
    (2, _("Day")),
]

DURATION_TO_MINUTES = [1, 60, 60 * 24]


class BaseStep(models.Model):

    """Step in the schema for a recipe, batch or brew. Steps for a
    batch are inherited from the recipe, but more steps may be
    added. The latter may be the case where a beer is normally
    packaged in kegs for a given recipe, but this time will be
    conditioned in a wood barrel.

    Steps are ordered within their parent.
    """

    temperature = models.FloatField(_("Temperature"), blank=True, null=True)
    duration = DurationField(_("Duration"), max_length=10)
    order = models.SmallIntegerField(null=True, blank=True)

    class Meta:

        abstract = True

    @property
    def total_duration(self):

        """Get the total duration of this step. This may be more than
        the duration property, for example when a mash step has a ramp
        up time in addition to a duration

        """


class RecipeStep(BaseStep):

    """ Step in the scheme for a recipe.
    """

    phase = models.ForeignKey("RecipePhase", on_delete=models.CASCADE)    
    recipe_step = models.ForeignKey("RecipeStep", null=True, blank=True,
                                    on_delete=models.SET_NULL)
    
    def __str__(self):

        return f"{self.phase} - {self.temperature}°C"

    class Meta:

        ordering = ["order"]


class BatchStep(BaseStep):

    """The batch step is inherited from the recipe, but may be changed
    within the batch. Also, more steps may be added to a batch, for
    instance steps involved with packaging.  The step within a batch
    is more focused on measuring than planning, so when the batch is
    produced, steps should be filled in with respect to actual start
    and end times.

    """

    phase = models.ForeignKey("BatchPhase", on_delete=models.CASCADE)
    start_time = models.DateTimeField(_("Start time"), null=True, blank=True)
    end_time = models.DateTimeField(_("End time"), null=True, blank=True)
    batch_step = models.ForeignKey("BatchStep", null=True, blank=True,
                                   on_delete=models.SET_NULL)

    def get_duration(self):

        """ Duration in minutes. This is the calculated duration, or if no
        times are filled in, the base duration"""

        try:
            return (self.end_time - self.start_time).seconds / 60
        except TypeError:
            return super().get_duration()

    class Meta:

        ordering = ["start_time"]
