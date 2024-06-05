from django.utils.translation import gettext_lazy as _
from django.http import HttpResponseRedirect
from django.forms import inlineformset_factory, HiddenInput
from django.urls import reverse
from django.contrib.contenttypes.forms import generic_inlineformset_factory
from django.contrib import messages
from .base import CreateView, UpdateView, DetailView
from ..models.brew import Brew
from ..models.batch import Batch
from ..models.metaphase import MetaPhase


class BrewDetailView(DetailView):

    """ Add phase vocab. TODO: could be a template_tag I guess """

    model = Brew
    can_log = True

    def phase_vocab(self):

        """ List phases defined for this system """

        return MetaPhase.objects.filter(parents__model="brew")


class BrewCreateView(CreateView):

    model = Brew

    def get_initial(self):

        """ Get initial form fields """

        if self.kwargs.get('batch'):
            return {'batch': Batch.objects.get(pk=self.kwargs['batch'])}

        return {}


class BrewUpdateView(UpdateView):

    model = Brew

    def get_form(self, form_class=None):

        form = super().get_form(form_class=form_class)

        form.fields['batch'].widget = HiddenInput()

        return form


class BrewImportPhasesView(DetailView):

    """ Get all brew phases from brewed beer """

    model = Brew

    @property
    def success_url(self):

        return reverse("view", kwargs={'pk': self.get_object().pk,
                                       'model': 'brew'})

    def get(self, request, *args, **kwargs):

        """ Shortcut to import of phases from recipe provided """

        if request.GET.get('recipe'):

            self.get_object().import_phases(request.GET['recipe'])
        else:
            messages.error(self.request, _("Recipe to import not provided."))

        return HttpResponseRedirect(self.success_url)
