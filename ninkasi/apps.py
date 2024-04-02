from django.apps import AppConfig
from django.forms import widgets
from .forms.dtinput import DateTimeInput
from .api import MashMetaPhase, MaturationMetaPhase, FermentationMetaPhase


class PhaseRegistry:

    """ Singleton registry holding possible (meta)phases """

    _registry = {}

    def __new__(cls):

        """ Creator ensuring singleton class """

        if not hasattr(cls, 'instance'):
            cls.instance = super(PhaseRegistry, cls).__new__(cls)
        return cls.instance

    @classmethod
    def register(cls, metaphase):

        """ Register MetaPhase by it's id """

        cls._registry[metaphase.id] = metaphase

    @classmethod
    def get_phase(cls, _id):

        """ Return the named metaphase """

        return cls._registry[_id]

    @classmethod
    def get_phases(cls):

        """ Get all possible phases """

        return cls._registry.values()


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
