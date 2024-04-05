from django.utils.translation import gettext_lazy as _
from django.http import HttpResponseRedirect
from django.forms import inlineformset_factory, HiddenInput
from django.contrib.contenttypes.forms import generic_inlineformset_factory
from .base import CreateView, UpdateView
from ..models.brew import Brew
from ..models.batch import Batch
from ..models.step import BatchStep
from ..models.transfer import Transfer


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
        #)

        #factory3 = generic_inlineformset_factory(
        #    Transfer, exclude=[],
        #    extra=1,
        #)

        kwargs = {}

        if self.request.method == "POST":
            kwargs['data'] = self.request.POST

        if self.object:
            kwargs['instance'] = self.object

        #formset_3 = factory3(**kwargs)
        #setattr(formset_3, "expanded", True)

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

        if self.kwargs.get('batch'):
            return {'batch': Batch.objects.get(pk=self.kwargs['batch'])}
        else:
            return {}


class BrewUpdateView(FormSetMixin, UpdateView):

    model = Brew
