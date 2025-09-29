""" All phase definitions """

from datetime import datetime
from django.db import models
from django.utils.translation import gettext_lazy as _
from django.contrib.contenttypes.fields import GenericForeignKey
from django.contrib.contenttypes.fields import GenericRelation
from django.contrib.contenttypes.models import ContentType
from django.conf import settings
from ninkasi.api import Phase as BasePhase
from ninkasi.duration import Duration
from .task import TaskFactory, MilestoneScheduledTask
from .unit import Unit
from .ingredient import Ingredient


class Phase(BasePhase, models.Model, TaskFactory):

    """Phases in the production process, relevant to the lifecycle of
    a batch or brew. This could be anything, from 'boil' to
    'maturation'. Definition of phases is part of the system setup and
    up to the brewer. However, usually the phases will reflect the
    standard process of: grind, mash, filter, boil, whirlpool, chill,
    ferment and mature. The phase is defined upon the batch and the
    brew but also recipe. Batch and brew import phases from the
    recipe.

    A phase is a task factory, that is there may be tasks attached to
    the phase defined by it's 'milestones': start and end.

    """

    parent = GenericForeignKey("content_type", "object_id")
    content_type = models.ForeignKey(ContentType, on_delete=models.CASCADE)
    object_id = models.PositiveIntegerField()
    order = models.PositiveIntegerField()
    metaphase = models.CharField(max_length=100, editable=False)

    tasks = GenericRelation("MilestoneTaskSub")

    def __str__(self):

        return self.name

    def __hash__(self):

        return self.pk

    def list_ingredients(self):

        return self.phaseingredient_set.all()

    def list_steps(self, raw=False):

        if raw:
            return self.step_set.all()

        return [step.get_real() for step in self.step_set.all()]

    def list_step_models(self):

        """ Return a list of models that may be added """

        return self.get_metaphase().list_step_models()

    def add_step(self, **kwargs):

        """ Add default step """

        model = self.get_metaphase().get_default_step_model()

        model.objects.create(phase=self, **kwargs)

    def has_steps(self):

        return self.step_set.exists()

    @property
    def name(self):

        """ Get the name from the metaphase """

        return self.get_metaphase().name

    def get_duration(self):

        """ Return total of all steps, or an empty duration """

        if self.list_steps(raw=True).exists():
            return sum(step.total_duration for step in self.list_steps())

        return Duration("0m")

    def copy(self, parent):

        """ Copy phase, but also all steps """

        new_phase = parent.phase.create(order=self.order,
                                        metaphase=self.metaphase)

        for step in self.list_steps():

            step.copy(new_phase)

        return new_phase

    def __eq__(self, thing):

        """ Determine equality. This needs to disregard the parent """

        if not self.__class__ == thing.__class__:

            return False

        if not (self.order == thing.order
                and self.metaphase == thing.metaphase):

            return False

        if self.step_set.count() != thing.list_steps(raw=True).count():
            return False

        steps_new = list(thing.list_steps())

        for idx, val in enumerate(self.list_steps()):

            if val != steps_new[idx]:
                return False

        return True

    def generate_tasks(self, **kwargs):

        """Generate any defined tasks if need be for the phase's
        milestones"""

        milestones = [f"ninkasi.{self.name}.start",
                      f"ninkasi.{self.name}.end"]

        self.tasks.all().delete()

        if self.parent._meta.model_name == "batch":

            for task in MilestoneScheduledTask.objects.filter(
                    milestone=milestones[0]):

                start = self.parent.get_phase_start(self.id)
                kwargs['name'] = f"{task.name} - {self.parent}"
                kwargs['parent'] = self.parent

                if start:

                    if isinstance(start, datetime):
                        kwargs['time'] = start.time()

                    task.generate_tasks(date=start, **kwargs)

    class Meta:

        app_label = "ninkasi"
        ordering = ["order"]
        verbose_name_plural = _("Phases")


class PhaseIngredient(models.Model):

    """Ingredients are related to a recipe phase with a given amount,
    but also a time to add. This allows for hop gifts to be specified,
    but also for example steeping malts.

    """

    # TODO: make sure that there is a conversion from given unit to
    # ingredient's default unit

    ingredient = models.ForeignKey(Ingredient, on_delete=models.CASCADE)
    amount = models.FloatField(_("Amount"))
    unit = models.ForeignKey(Unit, on_delete=models.CASCADE)
    addition_time = models.FloatField(default=0)
    phase = models.ForeignKey("Phase", on_delete=models.CASCADE)

    @property
    def name(self):

        return self.ingredient.name

    def __str__(self):

        return f"{self.ingredient} {self.amount}"
