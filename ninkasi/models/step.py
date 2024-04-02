from django.db import models
from django.utils.translation import gettext_lazy as _
from django.core.exceptions import ObjectDoesNotExist
from ..utils import class_implements
from .phase import Phase
from .fields import DurationField



DURATION_VOCAB = [
    (0, _("Minute")),
    (1, _("Hour")),
    (2, _("Day")),
]

DURATION_TO_MINUTES = [1, 60, 60 * 24]


class Step(models.Model):

    """Step in the schema for a recipe, batch or brew. Steps for a
    batch are inherited from the recipe, but more steps may be
    added. The latter may be the case where a beer is normally
    packaged in kegs for a given recipe, but this time will be
    conditioned in a wood barrel.

    Steps are ordered within their parent.
    """

    phase = models.ForeignKey("Phase", on_delete=models.CASCADE)
    temperature = models.FloatField(_("Temperature"), blank=True, null=True)
    duration = DurationField(_("Duration"), max_length=10)
    order = models.SmallIntegerField(default=0, editable=False)

    class Meta:

        app_label = "ninkasi"
        ordering = ["order"]

    def get_real(self):

        """See if there is an object there that is the actual
        implementation

        """

        for obj in self._meta.related_objects:

            try:
                real = getattr(self, obj.name)

                if class_implements(real.__class__, self.__class__):
                    return real
            except ObjectDoesNotExist:
                pass

        return self

    def get_total_duration(self):

        """Get the total duration of this step. This may be more than
        the duration property only, for example when a mash step has a
        ramp up time in addition to a duration

        """

        return self.duration

    def copy(self, parent, **kwargs):

        """ Copy self onto parent """

        kwargs.update({"order": self.order,
                       "duration": self.duration,
                       "temperature": self.temperature})

        return self.__class__.objects.create(phase=parent, **kwargs)

    def __eq__(self, thing):

        """ Check for equality. Disregard parent. """

        return (self.__class__ == thing.__class__
                and self.order == thing.order
                and self.duration == thing.duration
                and self.temperature == thing.temperature)


class MashStep(Step):

    """ Step for basic mash with heatup. Includes ramp-up time """

    rampup = DurationField(_("Ramp-up"), max_length=10)

    def __str__(self):

        return f"{ self.temperature } &deg;C"

    def get_total_duration(self):

        """ Get total duration """

        return self.duration + self.rampup

    def copy(self, parent, **kwargs):

        kwargs['rampup'] = self.rampup

        return super().copy(parent, **kwargs)

    def __eq__(self, thing):

        return super().__eq__(thing) and self.rampup == thing.rampup


class FermentationStep(MashStep):

    """ same, same """


class RecipeStep(Step):

    """ Step in the scheme for a recipe.
    """

    recipe_step = models.ForeignKey("RecipeStep", null=True, blank=True,
                                    on_delete=models.SET_NULL)

    def __str__(self):

        return f"{self.phase} - {self.temperature}°C"

    class Meta:

        ordering = ["order"]


class BatchStep(Step):

    """The batch step is inherited from the recipe, but may be changed
    within the batch. Also, more steps may be added to a batch, for
    instance steps involved with packaging.  The step within a batch
    is more focused on measuring than planning, so when the batch is
    produced, steps should be filled in with respect to actual start
    and end times.

    """

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
