from django.utils.translation import gettext_lazy as _
from django.forms import inlineformset_factory
from django.http import HttpResponseRedirect
from django.contrib.contenttypes.forms import generic_inlineformset_factory
from django.contrib import messages


class FormSetMixin:

    def get_form(self, form_class=None):

        form = super().get_form(form_class=form_class)

        # pop fields we don't wanna use

        return form

    @property
    def formsets(self):

        """ Add formsets for any field specified in m2m_fields """

        kwargs = {}

        if self.request.method == "POST":
            kwargs['data'] = self.request.POST

        if self.object:
            kwargs['instance'] = self.object

        factories = []

        for fname in getattr(self.object, 'm2m_fields', []):
            factory = inlineformset_factory(
                self.model, getattr(self.model, fname).through, exclude=[],
            )
            factories.append(factory(**kwargs))

        return [factory(**kwargs)]

    def form_valid(self, form):

        """ Save formsets as well """

        self.object = form.save()

        for _formset in self.formsets:
            if _formset.is_valid():
                _formset.save()

        return HttpResponseRedirect(self.get_success_url())
