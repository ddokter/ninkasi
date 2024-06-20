from django.utils.translation import gettext_lazy as _
from django.forms import inlineformset_factory
from django.http import HttpResponseRedirect
from django.contrib.contenttypes.forms import generic_inlineformset_factory
from django.contrib import messages


class FormSetMixin:

    def get_m2m_fields(self, model):

        """ Generate list of m2m fields that have a defined through """

        for field in model._meta.many_to_many:
            if not getattr(model, field.name).through._meta.auto_created:
                yield field.name

    def get_form(self, form_class=None):

        """We need to pop m2m fields from regular fields, to prevent
        the field to show up in the regular form fields.

        """

        form = super().get_form(form_class=form_class)

        for fname in self.get_m2m_fields(self.model):

            form.fields.pop(fname)

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

        for fname in self.get_m2m_fields(self.model):

            submodel = getattr(self.model, fname).through

            factory = inlineformset_factory(
                self.model, submodel, exclude=[],
                fk_name=getattr(submodel, "fk_name", None)
            )
            factories.append(factory(**kwargs))

        return factories

    def form_valid(self, form):

        """ Save formsets as well
        TODO: add error handling to ui
        """

        self.object = form.save()

        for _formset in self.formsets:
            if _formset.is_valid():
                _formset.save()

        return HttpResponseRedirect(self.get_success_url())
