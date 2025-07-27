from datetime import datetime
from django.views.generic import TemplateView
from ..models.task import (ScheduledTask, RepeatedScheduledTask, Task,
                           TaskFactory)
from ..models.brew import Brew
from .calendar import Calendar


class Home(TemplateView, Calendar):

    """ Dashboard """

    template_name = "index.html"

    def tasks_today(self):

        """ Return all tasks scheduled for today """

        day = datetime.now()

        return ScheduledTask.objects.for_date(day)

    def tasks_open(self):

        """ Return all tasks not cancelled or done """

        tasks = []

        for task in Task.objects.filter(status=0):

            task = task.get_real()

            if not isinstance(task, TaskFactory):

                tasks.append(task)

        return tasks

    def get_data(self):

        """ Get scheduled tasks for the week """

        data = {}

        for day in self.get_current_week()['days']:

            data[day] = [task.get_real() for task in
                         ScheduledTask.objects.for_date(day)]

        return data

    def get_current_week(self):

        return self.week

    def planned_brews(self):

        """ List all brews that are scheduled """\

        today = datetime.now()

        return Brew.objects.filter(date__gt=today)

    def get_current_brews(self):

        today = datetime.now()

        return Brew.objects.filter(date__date=today)

    def get(self, request, *args, **kwargs):

        """ Set the task to done """

        if 'fixtask' in request.GET:

            Task.objects.filter(pk=request.GET['fixtask']).update(status=1)

        return super().get(request, *args, **kwargs)
