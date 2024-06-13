""" Task definitions """

from datetime import datetime, date
from django.db import models
from django.utils.translation import gettext_lazy as _
from django.conf import settings
from django.contrib.contenttypes.fields import GenericForeignKey
from django.contrib.contenttypes.models import ContentType
from .fields import DurationField, EventField
from .base import BaseModel
from ..events import EventRegistry


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

                task.generate_tasks(date=_date)

        return self.get_queryset().filter(date=_date)


class TaskFactory:

    """Generates tasks that stay linked to the factory, so the same
    factory can generate those tasks again (and again). The factory is
    responsible for preventing inadvert copies.

    """

    def generate_tasks(self, **kwargs):

        """Generate tasks. If the method is called again, the factory
        is responsible for keeping track of already generated tasks, so
        no orphaned or useless tasks stay around."""


class Task(BaseModel):

    """Base class for tasks. Any actual task should be a subclass, so
    the get_real method may be used to get the actual task.

    """

    name = models.CharField(_("Name"), max_length=100)
    description = models.TextField(_("Description"))
    priority = models.SmallIntegerField(default=3,
                                        choices=PRIO_VOCAB)
    status = models.SmallIntegerField(default=0,
                                      editable=False,
                                      choices=STATUS_VOCAB)
    estimated_time = DurationField()

    @property
    def is_done(self):

        """ Shortcut to done status """

        return self.status == 1

    def __str__(self):

        real = self.get_real()

        if self == real:
            return self.name

        return f"{ str(real) } [{ real.get_status_display() }]"

    def get_details(self):

        """ Return a more detailed description of the task. This should
        be a tuple of (str, dict) """

        return (self.description, {})

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
    precision = DurationField()

    def get_deadline(self):

        """ Add precision to date (and if set, time) """

        deadline = self.date

        if self.time:
            deadline = datetime.combine(self.date, self.time)

        return deadline + self.precision.as_timedelta()

    def is_due(self):

        """Is the task due yet? This is the deadline compared to the
        current time or date.

        """

        deadline = self.get_deadline()

        if isinstance(deadline, datetime):
            return deadline < datetime.now()

        return deadline < date.today()

    class Meta:
        app_label = "ninkasi"


PRECISION_HELP = _("How much slack is allowed around the specified time?")


OFFSET_HELP = _("Offset from time of event. Use negative durations"
                " to specify before the event"
                )


def event_vocab():

    """ Provide vocabulary for events """

    return [(evt, evt) for evt in EventRegistry.list_events()]


class EventScheduledTask(Task, TaskFactory):

    """Task that is created based on an event. The precision field
    specifies how much slack there is around the scheduled time.
    Events are specified by Ninkasi and are in terms of 'tank empty',
    'batch start', etc.

    """

    precision = DurationField(help_text=PRECISION_HELP)
    event = EventField(max_length=100, choices=event_vocab)
    offset = DurationField(help_text=OFFSET_HELP, null=True, blank=True)

    def generate_tasks(self, **kwargs):

        """ Generate tasks based on the given event. The kwargs must
        contain a date and may contain a time. """

        if 'date' not in kwargs:
            raise KeyError("'date' must be specified in kwargs")

        self.eventtasksub_set.filter(
            name=kwargs['name'],
            object_id=kwargs['parent'].id,
            content_type=ContentType.objects.get_for_model(kwargs['parent']).id
        ).delete()

        kwargs.update(priority=self.priority,
                      precision=self.precision,
                      description=self.description
                      )

        return self.eventtasksub_set.create(**kwargs)

    def h10nized(self):

        """ Provide a human readable version"""

        sign = self.offset.get_sign()

        if sign == "-":
            sign = ""

        return _(f"{ self.name } within { self.precision } of { self.event } "
                 f"{ sign }{ self.offset }")

    class Meta:
        app_label = "ninkasi"


FREQUENCY_VOCAB = [(0, _("Daily")),
                   (1, _("Weekly")),
                   (2, _("Monthly")),
                   (3, _("Yearly"))]


class RepeatedScheduledTask(ScheduledTask, TaskFactory):

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

    def generate_tasks(self, **kwargs):

        """Spawn a concrete task from an abstract repeat for the
        given date, or update it, if it's already there.

        """

        kwargs.update(priority=self.priority, precision=self.precision)

        return self.repeatedtasksub_set.get_or_create(**kwargs)

    class Meta:
        app_label = "ninkasi"


class RepeatedTaskSub(ScheduledTask):

    """Implement the task that is spawned from a RepeatedScheduledTask
    whenever one needs to say something specific about one single
    instance, since a repeat is 'abstract'.

    """

    factory = models.ForeignKey(RepeatedScheduledTask,
                                on_delete=models.CASCADE)

    def __str__(self):

        return str(self.parent)


class EventTaskSub(ScheduledTask):

    """ Parented task created through planned event """

    factory = models.ForeignKey(EventScheduledTask, on_delete=models.CASCADE)

    parent = GenericForeignKey("content_type", "object_id")
    content_type = models.ForeignKey(ContentType, on_delete=models.CASCADE)
    object_id = models.PositiveIntegerField()

    def get_details(self):

        details = super().get_details()

        details[1]['event'] = self.factory.event

        return details
