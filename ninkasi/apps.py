from django.apps import AppConfig
from django.forms import widgets
from .forms.dtinput import DateTimeInput


class NinkasiConfig(AppConfig):

    name = 'ninkasi'

    def ready(self):

        widgets.DateTimeInput.input_type = 'datetime-local'
        widgets.DateInput.input_type = 'date'
        widgets.TimeInput.input_type = 'time'
