from django.http import HttpResponseRedirect
from django.urls import reverse
from .base import DetailView
from ..models.phase import Phase


class PhaseView(DetailView):

    model = Phase

    def step_vocab(self):

        """ List phases defined for this system """

        return [(model.split(".")[1], model) for model in
                self.object.list_step_models()]


class PhaseMoveStepView(PhaseView):

    @property
    def success_url(self):

        obj = self.get_object()

        return reverse("view", kwargs={
            'pk': obj.pk,
            'model': 'phase'})
    
    def get(self, request, *args, **kwargs):

        """ Shortcut to moving of steps """

        if kwargs.get('step'):

            parent = self.get_object()

            parent.move(kwargs['step'], request.GET.get('dir'))

        return HttpResponseRedirect(self.success_url)
