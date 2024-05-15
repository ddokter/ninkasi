from django.apps import AppConfig
from django.forms import widgets
from .forms.dtinput import DateTimeInput
from .api import MashMetaPhase, MaturationMetaPhase, FermentationMetaPhase
from .resource import ResourceRegistry
from .registry import PhaseRegistry


class NinkasiConfig(AppConfig):

    name = 'ninkasi'

    def ready(self):

        widgets.DateTimeInput.input_type = 'datetime-local'
        widgets.DateInput.input_type = 'date'
        widgets.TimeInput.input_type = 'time'

        registry = PhaseRegistry()

        registry.register(MashMetaPhase())
        registry.register(MaturationMetaPhase())
        registry.register(FermentationMetaPhase())

        # Register resource for style, prevent import error
        #
        # TODO: maybe make resource use get_model?
        #
        from .models.style import StyleResource

        ResourceRegistry.register("style", "django", StyleResource())
