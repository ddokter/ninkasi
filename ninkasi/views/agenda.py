from datetime import datetime
from django.views.generic import TemplateView
from django.utils import timezone
from ..models.task import ScheduledTask, RepeatedScheduledTask
from .calendar import Calendar


class AgendaView(TemplateView, Calendar):

    """The agenda view provides a monthly overview of tasks.

    """

    template_name = "agenda.html"

    def get_data(self):

        """ Show data for calendar. This may generate tasks on the fly, for
        repeated scheduled tasks."""

        data = {}

        for day in self.month['days']:

            data[day] = [task.get_real() for task in
                         ScheduledTask.objects.for_date(day)]

        return data
