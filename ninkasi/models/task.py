""" Task definitions """

from datetime import datetime, date
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


class ScheduledTaskManager(models.Manager):

    """ Taskmanager that can generate on the fly tasks in case of repeated
    tasks """

    def for_date(self, _date):

        """Return a list of tasks for the given day. If the task
        retrieved is a repeated task, generate specific tasks on the
        fly.

        """

        for task in RepeatedScheduledTask.objects.filter(date__lt=_date):
            if task.is_due_date(_date):

                task.spawn(_date)

        return self.get_queryset().filter(date=_date)


class Task(BaseModel):

    """Base class for tasks. A task may be related to the apparatus of
    the brewery, or may be stand-alone.

    """

    name = models.CharField(_("Name"), max_length=100)
    description = models.TextField(_("Description"))
    priority = models.SmallIntegerField(default=3,
                                        choices=PRIO_VOCAB)
    status = models.SmallIntegerField(default=0,
                                      editable=False,
                                      choices=STATUS_VOCAB)

    @property
    def is_done(self):

        """ Shortcut to done status """

        return self.status == 1

    def __str__(self):

        real = self.get_real()

        if self == real:
            return self.name

        return f"{ str(real) } [{ real.get_status_display() }]"

    class Meta:
        app_label = "ninkasi"


class ScheduledTask(Task):

    """Task that is set for a specific time and date. The precision
    field specifies how much slack there is around the scheduled
    time.

    """

    objects = ScheduledTaskManager()

    date = models.DateField()
    time = models.TimeField(blank=True, null=True)
    precision = DurationField(max_length=5)

    def get_deadline(self):

        """ Add precision to date (and if set, time) """

        deadline = self.date

        if self.time:
            deadline = datetime.combine(self.date, self.time)

        return deadline + self.precision.as_timedelta()

    def is_due(self):

        deadline = self.get_deadline()

        if isinstance(deadline, datetime):
            return deadline < datetime.now()

        return deadline < date.today()

    class Meta:
        app_label = "ninkasi"


EVENT_VOCAB = [(0, _("Container empty")),
               (1, _("Container fill")),
               (2, _("Brew start")),
               (3, _("Brew finish"))]


PRECISION_HELP = _("Use negative durations to specify before.")


class EventScheduledTask(Task):

    """Task that is created based on an event. The precision field
    specifies how much slack there is around the scheduled time.
    Events are specified by Ninkasi.

    TODO: somehow list events, maybe in a registry?
    """

    event = models.SmallIntegerField(choices=EVENT_VOCAB)
    precision = DurationField(max_length=10,
                              help_text=PRECISION_HELP)

    def __str__(self):

        if self.precision.amount < 0:
            return (f"{ self.name } { self.precision.abs() } before"
                    f" { self.get_event_display() }")

        return (f"{ self.name } within { self.precision } after "
                f"{ self.get_event_display() }")

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

    def set_status(self, status, _date):

        """ Set the status for this task for the given date. This is the
        moment to spawn an actual task. """

    def is_due_date(self, _date):

        """ Check whether the task should be done on this date """

        if self.date == _date:
            return True

        if self.frequency == 0:
            return True

        if self.frequency == 1:
            if (
                    abs((self.date - _date.date()).days) %
                    (7 * self.frequency_modifier) == 0):
                return True

        # TODO: implement monthly and yearly
        return False

    def spawn(self, _date):

        return self.repeatedtasksub_set.get_or_create(
            date=_date, priority=self.priority, precision=self.precision)

    class Meta:
        app_label = "ninkasi"


class RepeatedTaskSub(ScheduledTask):

    """Implement the task that is spawned from a
    RepeatedScheduledTask whenever one needs to say something specific
    about one single instance

    """

    parent = models.ForeignKey(RepeatedScheduledTask, on_delete=models.CASCADE)

    def __str__(self):

        return str(self.parent)
