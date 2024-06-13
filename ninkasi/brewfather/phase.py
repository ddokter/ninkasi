""" Brewfather implementatins for phase and steps """

from django.core.exceptions import ValidationError
from ninkasi import api
from ninkasi.duration import Duration


class Phase(api.Phase):

    """ Brewfather implementation of phase """

    def __init__(self, metaphase):

        self.metaphase = metaphase
        self.steps = []
        self.order = 0
        self.mode = 'ro'

    @property
    def id(self):

        return str(self)

    def __str__(self):

        return self.metaphase

    def add_step(self, step):

        """ Add step and keep order."""

        self.steps.append(step)

    def list_steps(self, raw=False):

        return self.steps

    def has_steps(self):

        return len(self.steps)

    def copy(self, parent):

        """ Copy onto parent, that must be a django Model """

        new_phase = parent.phase.create(order=self.order,
                                        metaphase=self.metaphase)

        for step in self.list_steps():

            step.copy(new_phase)

        return new_phase

    def get_duration(self):

        """ Get duration of this phase. """

        return (sum(step.duration for step in self.list_steps()) or
                Duration("0m"))


class StepMixin:

    """ Provide step basics """

    order = 0
    mode = 'ro'

    def copy(self, parent, **kwargs):

        """ Copy self onto parent """

        kwargs.update({
            "name": self.name,
            "order": self.order,
            "duration": self.duration,
            "temperature": self.temperature})

        return parent.add_step(**kwargs)

    @property
    def temperature(self):

        """ Return step temperature """

        return self.data['stepTemp']

    @property
    def duration(self):

        """ Unimplemented """

    def __str__(self):

        return self.name


class MashStep(StepMixin, api.Step):

    """ Step wrapper """

    def __init__(self, data):

        self.data = data

    def __str__(self):

        return f"{ self.temperature } &deg;C"

    @property
    def duration(self):

        return Duration(f"{ self.data['stepTime'] }m")


BoilStep = MashStep


class FermentationStep(StepMixin, api.Step):

    """ Step wrapper for fermentation """

    def __init__(self, data):

        self.data = data

    @property
    def name(self):

        return self.data['type']

    @property
    def duration(self):

        return Duration(f"{ self.data['stepTime'] }d")


class FilterStep(StepMixin, api.Step):

    def __init__(self, **kwargs):

        self._data = kwargs

    @property
    def name(self):

        return self._data['name']

    @property
    def temperature(self):

        return self._data['temperature']

    @property
    def duration(self):

        return self._data['duration']


class WhirlpoolStep(FilterStep):

    """ same. """
