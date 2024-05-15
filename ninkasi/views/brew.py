from django.utils.translation import gettext_lazy as _
from django.http import HttpResponseRedirect
from django.forms import inlineformset_factory, HiddenInput
from django.urls import reverse
from django.contrib.contenttypes.forms import generic_inlineformset_factory
from django.contrib import messages
from .base import CreateView, UpdateView, DetailView
from ..models.brew import Brew
from ..models.batch import Batch


class FormSetMixin:

    def get_form(self, form_class=None):

        form = super().get_form(form_class=form_class)

        form.fields['batch'].widget = HiddenInput()

        form.fields.pop('material')
        # form.fields.pop('tank')

        return form

    @property
    def formsets(self):

        """ Return all formsets for the brew. That amounts to a whopping 3 """

        factory1 = inlineformset_factory(
            Brew, Brew.material.through, exclude=[],
        )

        # factory2 = generic_inlineformset_factory(
        #    BatchStep, exclude=[],
        #    can_order=True
        # )

        # factory3 = generic_inlineformset_factory(
        #    Transfer, exclude=[],
        #    extra=1,
        # )

        kwargs = {}

        if self.request.method == "POST":
            kwargs['data'] = self.request.POST

        if self.object:
            kwargs['instance'] = self.object

        # formset_3 = factory3(**kwargs)
        # setattr(formset_3, "expanded", True)

        return [factory1(**kwargs)]

    def form_valid(self, form):

        self.object = form.save()

        for _formset in self.formsets:
            if _formset.is_valid():
                _formset.save()

        return HttpResponseRedirect(self.get_success_url())


class BrewCreateView(FormSetMixin, CreateView):

    model = Brew

    def get_initial(self):

        """ Get initial form fields """

        if self.kwargs.get('batch'):
            return {'batch': Batch.objects.get(pk=self.kwargs['batch'])}

        return {}


class BrewUpdateView(FormSetMixin, UpdateView):

    model = Brew


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
