from .base import CreateView, UpdateView
from ..models.sample import Sample
from ..forms.batchtank import DateTimeInput
# TODO: move this widget somewhere else


class SampleCreateView(CreateView):

    model = Sample

    def get_form(self, form_class=None):

        form = super().get_form(form_class=form_class)

        form.fields['date'].widget = DateTimeInput()
        
        return form
