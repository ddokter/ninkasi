from .base import DetailView
from ..models.task import Task


class FixTask(DetailView):

    model = Task

    """ Set task to done. TODO: this should be done Ajax style """

    def get(self, request, *args, **kwargs):
        """ Set the task to done """

        if kwargs.get('pk'):

            Task.objects.filter(pk=kwargs['pk']).update(status=1)

        return super().get(request, *args, **kwargs)
