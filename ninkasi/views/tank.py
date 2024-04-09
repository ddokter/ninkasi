from django.utils.translation import gettext_lazy as _
from django.http import HttpResponseRedirect
from django.forms import inlineformset_factory
from .base import CreateView, UpdateView
from ..models.tank import Tank
from ..models.task import Task


class FormSetMixin:

    def get_form(self, form_class=None):

        form = super().get_form(form_class=form_class)

        #form.fields.pop('maintenance_schema')

        return form

    @property
    def formsets(self):

        """ Return all formsets for the brew. That amounts to a whopping 3 """

        factory1 = inlineformset_factory(
            Tank, Tank.maintenance_schema.through, exclude=[],
        )

        kwargs = {}

        if self.request.method == "POST":
            kwargs['data'] = self.request.POST

        if self.object:
            kwargs['instance'] = self.object
        return [factory1(**kwargs)]

    def form_valid(self, form):

        self.object = form.save()

        for _formset in self.formsets:
            if _formset.is_valid():
                _formset.save()

        return HttpResponseRedirect(self.get_success_url())


class TankCreateView(FormSetMixin, CreateView):

    model = Tank


class TankUpdateView(FormSetMixin, UpdateView):

    model = Tank
