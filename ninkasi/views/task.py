from .base import DetailView
from ..models.task import Task


class FixTask(DetailView):

    model = Task

    """ Set task to done. TODO: this should be done Ajax style """

    def get(self, request, *args, **kwargs):

        """ Shortcut to moving of phases """

        if kwargs.get('task'):

            Task.objects.filter(pk=kwargs['task']).update(status=1)

        return super().get(request, *args, **kwargs)
