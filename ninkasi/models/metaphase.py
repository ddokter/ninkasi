""" Metaphase definition """

from django.db import models
from django.utils.translation import gettext_lazy as _
from ..events import EventProvider


class MetaPhase(models.Model, EventProvider):

    """MetaPhases are used to define what phases may occur in the
    brewing process. Typically this would be stuff like 'mash',
    'boil', 'fermentation' and 'maturation'. The metaphase also
    defines the classes of steps that may be added to the phase in the
    brew or batch.
    """

    name = models.CharField(unique=True, max_length=100)
    steps = models.ManyToManyField(
        "contenttypes.ContentType",
        limit_choices_to=models.Q(app_label="ninkasi",
                                  model__icontains="step")
    )
    default_step = models.ForeignKey(
        "contenttypes.ContentType",
        related_name="default_metaphase",
        on_delete=models.CASCADE,
        limit_choices_to=models.Q(app_label="ninkasi",
                                  model__icontains="step")
    )
    parents = models.ManyToManyField(
        "contenttypes.ContentType",
        related_name="mp_parents",
        limit_choices_to=models.Q(app_label="ninkasi",
                                  model__in=["batch", "brew", "recipe"])
    )

    def __str__(self):

        return self.name

    def list_parent_models(self):

        """ Show what parents are possible for this phase. """

        return self.parents.all()

    def list_step_models(self):

        """ return a list of step models that may be added to this phase.
        The returned steps are actually ContentTypes """

        return self.steps.all()

    def get_default_step_model(self):

        """ Get the step model for this meta """

        return self.default_step.model_class()

    def list_events(self):

        """The metaphase is an event provider, but per instance"""

        return [f"ninkasi.{ self.name }.start", f"ninkasi.{ self.name }.end"]

    class Meta:

        app_label = "ninkasi"
        ordering = ["name"]
        verbose_name_plural = _("MetaPhases")
