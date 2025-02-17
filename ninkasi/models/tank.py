from django.db import models
from django.utils.translation import gettext_lazy as _
from .container import Container
from ..milestones import MilestoneProviderModel
from ..tanks import Tank as BaseTank


class Tank(Container, MilestoneProviderModel, BaseTank):

    """Container for brew. May be any type of tank that holds beer in
    any stage of the process, i.e. CCT, BBT, lagertank. Subclass
    nikasi,Tank and your model should show up in 'Add' lists.

    """

    def __str__(self):

        return f"{ self.get_real().__class__.__name__ } { self.name }"

    @classmethod
    def list_milestones(cls):

        """Tanks provide milestones in the scheme of things: fill and
        empty"""

        return [f"ninkasi.{ cls._meta.model_name }.fill",
                f"ninkasi.{ cls._meta.model_name }.empty"]

    def content(self, date):

        """Return the batch that is in the tank on the given date, if
        at all.

        """

        if self.batchcontainer_set.filter(
                from_date__date__lte=date, to_date__date__gte=date).exists():
            return self.batchcontainer_set.filter(
                from_date__date__lte=date,
                to_date__date__gte=date).first().batch

        return None

    def list_tasks(self):

        """ List all tasks for this tank. This is the list of tasks in the
        maintenance schema. """

        return []

    class Meta:

        app_label = "ninkasi"
        ordering = ["name"]
        verbose_name_plural = _("Tanks")


class BBT(Tank):

    """Bright beer tank

    """

    class Meta:

        app_label = "ninkasi"
        verbose_name_plural = _("BBTs")


class CCT(Tank):

    """ Conical-cylindrical tank """

    cone_loss = models.SmallIntegerField(_("Amount lost in cone."))

    class Meta:

        app_label = "ninkasi"
        verbose_name_plural = _("CCTs")


class LagerTank(Tank):

    """ Lager tank """

    class Meta:

        app_label = "ninkasi"
        verbose_name_plural = _("Lager tanks")
