from django.db import models
from django.utils.translation import gettext_lazy as _
from .container import Container
from ..milestones import MilestoneProviderModel


TTYPE_VOCAB = [
    (0, "Fermentation"),
    (1, "BBT"),
    (2, "Lagering")
]


class Tank(Container):

    """Container for brew. May be any type of tank that holds beer in
    any stage of the process, i.e. CCT, BBT, lagertank.

    """

    ttype = models.SmallIntegerField(_("Type"),
                                     default=0,
                                     choices=TTYPE_VOCAB,
                                     )

    def __str__(self):

        return self.name

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

        return self.maintenance_schema.all()

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


class CCT(Tank, MilestoneProviderModel):

    """ Conical-cylindrical tank """

    cone_loss = models.SmallIntegerField(_("Amount lost in cone."))

    @classmethod
    def list_milestones(cls):

        """The metaphase is an milestone provider, but per instance"""

        return ["ninkasi.cct.fill", "ninkasi.cct.empty"]

    class Meta:

        app_label = "ninkasi"
        verbose_name_plural = _("CCTs")


class LagerTank(Tank):

    """ Lager tank """

    class Meta:

        app_label = "ninkasi"
        verbose_name_plural = _("Lager tanks")
