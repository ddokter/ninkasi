from django.http import HttpResponseRedirect
from django.urls import reverse
from django.apps import apps
from django.contrib import messages
from django.utils.translation import gettext_lazy as _
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


class AddPhaseView(DetailView):

    """ Add phase to parent """

    def get_object(self):

        """ Override to get model from kwargs """

        _model = apps.get_model("ninkasi", self.kwargs['model'])

        return _model.objects.get(id=self.kwargs['pk'])

    @property
    def success_url(self):

        return reverse("view", kwargs={'pk': self.get_object().pk,
                                       'model': self.kwargs['model']})

    def get(self, request, *args, **kwargs):

        """ Shortcut to creation of phases """

        if kwargs.get('phase'):

            self.get_object().add_phase(kwargs['phase'])
        else:
            messages.error(self.request, _("MetaPhase not provided."))

        return HttpResponseRedirect(self.success_url)


class MovePhaseView(AddPhaseView):

    """ Move phase in parent container """

    def get(self, request, *args, **kwargs):

        """ Shortcut to moving of phases """

        if kwargs.get('phase'):

            parent = self.get_object()

            parent.move(kwargs['phase'], request.GET.get('dir'), 'phase')

        return HttpResponseRedirect(self.success_url)
