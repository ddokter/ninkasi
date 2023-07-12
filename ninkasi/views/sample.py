from django.utils.translation import gettext_lazy as _
from django.http import HttpResponseRedirect
from django.forms import inlineformset_factory, HiddenInput
from django.forms.models import ModelChoiceIterator
from django.contrib.contenttypes.models import ContentType
from .base import CreateView, UpdateView
from ..models.sample import Sample
from ..models.batch import Batch
from ..models.measurement import Measurement
from ..forms.dtinput import DateTimeInput


class FormSetMixin:

    def get_form(self, form_class=None):

        form = super().get_form(form_class=form_class)

        # form.fields.pop('measurement')

        return form

    @property
    def formset_label(self):

        return _("Measurements")

    @property
    def formsets(self):

        factory = inlineformset_factory(
            Sample, Measurement, exclude=[],
            #widgets={'date_from': DateTimeInput(),
            #         'date_to': DateTimeInput()}
            )

        kwargs = {}

        if self.request.method == "POST":
            kwargs['data'] = self.request.POST

        if self.object:
            kwargs['instance'] = self.object

        return [factory(**kwargs)]

    def form_valid(self, form):

        self.object = form.save()

        for _formset in self.formsets:

            if _formset.is_valid():
                _formset.save()

        return HttpResponseRedirect(self.get_success_url())


class SampleCreateView(FormSetMixin, CreateView):

    model = Sample
    expanded_formset = True

    def get_initial(self):

        if self.kwargs.get('batch'):

            batch = Batch.objects.get(pk=self.kwargs['batch'])
            
            return {'batch': batch,
                    'content_type': ContentType.objects.get(
                        app_label="ninkasi", model="batch"),
                    'object_id': batch.id
                    }
        else:
            return {}

    def get_form(self, form_class=None):

        form = super().get_form(form_class=form_class)

        form.fields['date'].widget = DateTimeInput()

        if self.kwargs.get('batch'):
            batch = Batch.objects.get(pk=self.kwargs['batch'])

            form.fields['content_type'].widget = HiddenInput()
            form.fields['object_id'].widget = HiddenInput()

            form.fields['step'].widget.choices.queryset = batch.step.all()

        return form


class SampleUpdateView(FormSetMixin, UpdateView):

    model = Sample
    expanded_formset = True

    def get_initial(self):

        if self.kwargs.get('batch'):
            return {'batch': Batch.objects.get(pk=self.kwargs['batch'])}
        else:
            return {}

    def get_form(self, form_class=None):

        form = super().get_form(form_class=form_class)

        form.fields['date'].widget = DateTimeInput()
        form.fields['content_type'].widget = HiddenInput()
        form.fields['object_id'].widget = HiddenInput()

        if self.kwargs.get('batch'):
            batch = Batch.objects.get(pk=self.kwargs['batch'])
            
            form.fields['step'].widget.choices.queryset = batch.step.all()

        return form
