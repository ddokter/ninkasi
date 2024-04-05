from django.db import models
from django.utils.translation import gettext_lazy as _


PRIO_VOCAB = [(1, _("High")),
              (3, _("Medium")),
              (5, _("Low"))]


class Task(models.Model):

    """Base class for tasks. A task may be related to the apparatus of
    the brewery, or may be stand-alone.

    """

    name = models.CharField(_("Name"), max_length=100)
    description = models.TextField(_("Description"))
    priority = models.SmallIntegerField(default=3,
                                        choices=PRIO_VOCAB)

    def __str__(self):

        return self.name

    class Meta:
        app_label = "ninkasi"
        abstract = True


class ScheduledTask(Task):

    """ Task that is set for a specific time and date """

    date = models.DateField()
    time = models.TimeField(blank=True, null=True)

    class Meta:
        app_label = "ninkasi"
