from django.db import models
from django.utils.translation import gettext_lazy as _
from django.contrib.contenttypes.fields import GenericForeignKey
from django.contrib.contenttypes.models import ContentType
from django.conf import settings
from ninkasi.apps import PhaseRegistry
from .ordered import OrderedContainer


class BasePhase(OrderedContainer):

    """Base class for defining phases. Extend this class for
    implementing any type of phase. Class must support deepcopy.

    """

    def get_duration(self):

        """ Return total of all steps """

        return sum(step.get_total_duration() for step in self.list_steps())

    def list_steps(self, raw=False):

        """ Return list of all steps for this phase. If raw is True
        do not look for actual implementation of the steps."""

    def get_child_qs(self):

        return self.list_steps(raw=True)

    def copy(self, parent):

        """ Provide a deep copy of self onto parent """

    def __eq__(self, thing):

        """ Determine whether the phases are equal """


class Phase(models.Model, BasePhase):

    """Phases in the production process, relevant to the lifecycle of
    a batch or brew. This could be anything, from 'boil' to
    'maturation'. Defintion of phases is part of the system setup and
    up to the brewer. However, usually the phases will reflect the
    standard process of: grind, mash, filter, boil, whirlpool, chill,
    ferment and mature. The phase is defined upon the batch, brew but
    also recipe.

    """

    parent = GenericForeignKey("content_type", "object_id")
    content_type = models.ForeignKey(ContentType, on_delete=models.CASCADE)
    object_id = models.PositiveIntegerField()
    order = models.PositiveIntegerField()
    metaphase = models.CharField(max_length=100, editable=False)

    def get_metaphase(self):

        """ Return asociated meta phase """

        return PhaseRegistry.get_phase(self.metaphase)

    def __str__(self):

        return self.name

    def list_steps(self, raw=False):

        if raw:
            return self.step_set.all()

        return [step.get_real() for step in self.step_set.all()]

    def list_step_models(self):

        """ Return a list of models that may be added """

        return self.get_metaphase().list_step_models()

    @property
    def name(self):

        """ Get the name from the metaphase """

        return self.get_metaphase().name

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

        if (self.list_steps(raw=True).count()
            != thing.list_steps(raw=True).count()):
            return False

        steps_old = list(self.list_steps())
        steps_new = list(thing.list_steps())

        for i in range(len(steps_old)):

            if steps_old[i] != steps_new[i]:
                return False

        return True

    class Meta:

        app_label = "ninkasi"
        ordering = ["order"]
        verbose_name_plural = _("Phases")
