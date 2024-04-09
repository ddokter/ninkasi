""" Task definitions """

from django.db import models
from django.utils.translation import gettext_lazy as _
from .fields import DurationField
from .base import BaseModel


PRIO_VOCAB = [(1, _("High")),
              (3, _("Medium")),
              (5, _("Low"))]

STATUS_VOCAB = [(0, _("Open")),
                (1, _("Done")),
                (2, _("Cancelled")),
                (3, _("Forfeited"))]


class Task(BaseModel):

    """Base class for tasks. A task may be related to the apparatus of
    the brewery, or may be stand-alone.

    """

    name = models.CharField(_("Name"), max_length=100)
    description = models.TextField(_("Description"))
    priority = models.SmallIntegerField(default=3,
                                        choices=PRIO_VOCAB)
    status = models.SmallIntegerField(default=0,
                                      choices=STATUS_VOCAB)

    def __str__(self):

        real = self.get_real()

        if self == real:
            return self.name

        return str(real)

    class Meta:
        app_label = "ninkasi"


class ScheduledTask(Task):

    """Task that is set for a specific time and date. The precision
    field specifies how much slack there is around the scheduled
    time.

    """

    date = models.DateField()
    time = models.TimeField(blank=True, null=True)
    precision = DurationField(max_length=5)

    def get_deadline(self):

        """ Add precision to date (and if set, time) """

        deadline = self.date

        # TODO: Add time

        return deadline + self.precision.as_timedelta()

    class Meta:
        app_label = "ninkasi"


EVENT_VOCAB =[(0, _("Container empty")),
              (1, _("Container fill")),
              (2, _("Brew start")),
              (3, _("Brew finish"))]


class EventScheduledTask(Task):

    """Task that is created based on an event. The precision field
    specifies how much slack there is around the scheduled time.
    Events are specified by Ninkasi.

    TODO: somehow list events, maybe in a registry?
    """

    event = models.SmallIntegerField(choices=EVENT_VOCAB)
    precision = DurationField(max_length=5)

    def __str__(self):

        return f"""{ self.name } within { self.precision } of
                   { self.get_event_display() }"""

    def get_deadline(self):

        """ Add precision to date (and if set, time) """

    class Meta:
        app_label = "ninkasi"


FREQUENCY_VOCAB = [(0, _("Daily")),
                   (1, _("Weekly")),
                   (2, _("Monthly")),
                   (3, _("Yearly"))]


class RepeatedScheduledTask(ScheduledTask):

    """Task that is scheduled upon a frequency, based from a start
    date.  The frequency is taken from a vocabulary, that may be
    modified, to, for instance, specify once per two months.

    """

    frequency = models.SmallIntegerField(choices=FREQUENCY_VOCAB)
    frequency_modifier = models.SmallIntegerField(
        default=1,
        help_text=_("For instance, to specify 'every two weeks'")
    )

    def is_due_date(self, date):

        """ Check whether the task should be done on this date """

        if self.date == date:
            return True

        if self.frequency == 0:
            return True

        if self.frequency == 1:
            if (abs((self.date - date.date()).days) %
                (7 * self.frequency_modifier) == 0):
                return True

        # TODO: implement monthly and yearly
        return False

    class Meta:
        app_label = "ninkasi"
