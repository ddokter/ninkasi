from datetime import datetime
from django.views.generic import TemplateView
from ..models.task import (ScheduledTask, RepeatedScheduledTask, Task,
                           TaskFactory)


class Home(TemplateView):

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


class FixTask(Home):

    """ Set task to done. TODO: this should be done Ajax style """

    def get(self, request, *args, **kwargs):

        """ Shortcut to moving of phases """

        if kwargs.get('task'):

            Task.objects.filter(pk=kwargs['task']).update(status=1)

        return super().get(request, *args, **kwargs)
