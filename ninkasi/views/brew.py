from django.utils.translation import gettext_lazy as _
from django.http import HttpResponseRedirect
from django.forms import inlineformset_factory, HiddenInput
from django.contrib.contenttypes.forms import generic_inlineformset_factory
from .base import CreateView, UpdateView
from ..models.brew import Brew
from ..models.batch import Batch
from ..models.step import Step
from ..forms.dtinput import DateTimeInput


class FormSetMixin:

    def get_form(self, form_class=None):

        form = super().get_form(form_class=form_class)

        form.fields['batch'].widget = HiddenInput()

        form.fields.pop('asset')
        form.fields.pop('step')
        form.fields.pop('tank')

        form.fields['date'].widget = DateTimeInput()

        return form

    @property
    def formsets(self):

        factory1 = inlineformset_factory(
            Brew, Brew.asset.through, exclude=[],
        )

        factory2 = inlineformset_factory(
            Brew, Brew.step.through, exclude=[],
            widgets={'start_time': DateTimeInput(),
                     'end_time': DateTimeInput()
                     },
            can_order=True
        )

        factory3 = inlineformset_factory(
            Brew, Brew.tank.through, exclude=[],
            widgets={'date': DateTimeInput()},
            extra=1,
        )

        kwargs = {}

        if self.request.method == "POST":
            kwargs['data'] = self.request.POST

        if self.object:
            kwargs['instance'] = self.object

        formset_3 = factory3(**kwargs)
        setattr(formset_3, "expanded", True)
            
        return [factory1(**kwargs), factory2(**kwargs), formset_3]

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
