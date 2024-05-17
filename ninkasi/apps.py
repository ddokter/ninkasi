from django.apps import AppConfig
from django.forms import widgets
from .forms.dtinput import DateTimeInput
from .resource import ResourceRegistry


class NinkasiConfig(AppConfig):

    name = 'ninkasi'

    def ready(self):

        widgets.DateTimeInput.input_type = 'datetime-local'
        widgets.DateInput.input_type = 'date'
        widgets.TimeInput.input_type = 'time'

        # Register resource for style, prevent import error
        #
        # TODO: maybe make resource use get_model?
        #
        from .models.style import StyleResource

        ResourceRegistry.register("style", "django", StyleResource())
