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

        """ Generate data for calendar. Loop over tanks and brewhouses,
        and display the calendar. """

        data = {}
        
        for mday in self.month['days']:

            day = datetime(self.month['year'], self.month['month'], mday,
                           tzinfo=timezone.get_current_timezone())

            data[mday] = list(ScheduledTask.objects.filter(date=day))

            for task in RepeatedScheduledTask.objects.filter(date__lt=day):
                if task.is_due_date(day):
                    data[mday].append(task)
            
        return data
