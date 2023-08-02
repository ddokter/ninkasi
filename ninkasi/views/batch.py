from django.utils.translation import gettext_lazy as _
from django.http import HttpResponseRedirect
from django.forms import inlineformset_factory
from django.contrib.contenttypes.forms import generic_inlineformset_factory
from .base import CreateView, UpdateView
from ..forms.dtinput import DateTimeInput
from ..forms.colorpicker import ColorInput
from ..models.batch import Batch
from ..models.recipe import Recipe
from ..models.step import Step


class FormSetMixin:

    def get_form(self, form_class=None):

        form = super().get_form(form_class=form_class)

        form.fields['deliverydate'].widget = DateTimeInput()
        form.fields['color'].widget = ColorInput()

        form.fields.pop('asset')
        form.fields.pop('step')
        form.fields.pop('tank')        

        return form

    @property
    def formset_label(self):

        return _("Assets")

    @property
    def formsets(self):

        factory1 = inlineformset_factory(
            Batch, Batch.asset.through, exclude=[])

        factory2 = inlineformset_factory(
            Batch, Batch.step.through, exclude=[],
            widgets={'start_time': DateTimeInput(),
                     'end_time': DateTimeInput()
                     }            
        )

        kwargs = {}

        if self.request.method == "POST":
            kwargs['data'] = self.request.POST

        if self.object:
            kwargs['instance'] = self.object
            
        return [factory1(**kwargs), factory2(**kwargs)]

    def form_valid(self, form):

        """ Check the form and all formsets """

        self.object = form.save()

        for _formset in self.formsets:
            if _formset.is_valid():
                _formset.save()

        return HttpResponseRedirect(self.get_success_url())


class BatchCreateView(FormSetMixin, CreateView):

    model = Batch


    def get_initial(self):

        if self.kwargs.get('recipe'):
            return {'recipe': Recipe.objects.get(pk=self.kwargs['recipe'])}
        else:
            return {}


class BatchUpdateView(FormSetMixin, UpdateView):

    model = Batch
