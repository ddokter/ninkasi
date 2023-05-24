from django.utils.translation import gettext_lazy as _
from django.http import HttpResponseRedirect
from django.forms import inlineformset_factory
from .base import CreateView, UpdateView
from ..models.batch import Batch
from ..forms.batchtank import DateTimeInput


class FormSetMixin:

    def get_form(self, form_class=None):

        form = super().get_form(form_class=form_class)

        form.fields.pop('tank')

        return form

    @property
    def formset_label(self):

        return _("Tanks")

    @property
    def formset(self):

        factory = inlineformset_factory(
            Batch, Batch.tank.through, exclude=[],
            widgets={'date_from': DateTimeInput(),
                     'date_to': DateTimeInput()}
            )

        kwargs = {}

        if self.request.method == "POST":
            kwargs['data'] = self.request.POST

        if self.object:
            kwargs['instance'] = self.object

        return factory(**kwargs)

    def form_valid(self, form):

        self.object = form.save()

        _formset = self.formset

        if _formset.is_valid():
            _formset.save()

        return HttpResponseRedirect(self.get_success_url())


class BatchCreateView(FormSetMixin, CreateView):

    model = Batch


class BatchUpdateView(FormSetMixin, UpdateView):

    model = Batch
