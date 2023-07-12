from django.utils.translation import gettext_lazy as _
from django.http import HttpResponseRedirect
from django.forms import inlineformset_factory, HiddenInput
from django.urls import reverse
from .base import CreateView, UpdateView
from ..models.batch import Transfer, Batch
from ..forms.dtinput import DateTimeInput


#class TransferView(FormSetMixin, UpdateView):
class TransferView(CreateView):

    model = Transfer

    def get_form(self, form_class=None):

        form = super().get_form(form_class=form_class)

        form.fields['date'].widget = DateTimeInput()
        form.fields['batch'].widget = HiddenInput()

        return form

    def get_initial(self):

        """If batch is in the initial arguments of the url, set it on
        the form

        """

        if self.kwargs.get('batch'):
            return {'batch': Batch.objects.get(pk=self.kwargs['batch'])}

        return {}


    @property
    def action_url(self):

        return "."


    @property
    def success_url(self):

        try:
            return reverse("view", kwargs={'model': 'batch',
                                           'pk': self.object.batch.id})
        except AttributeError:
            return super().success_url
