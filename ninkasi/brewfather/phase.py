""" Brewfather implementatins for phase and steps """

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

    def copy(self, parent):

        """ Copy onto parent, that must be a django Model """

        new_phase = parent.phase.create(order=self.order,
                                        metaphase=self.metaphase)

        for step in self.list_steps():

            step.copy(new_phase)

        return new_phase


class StepMixin:

    """ Provide step basics """

    order = 0

    def copy(self, parent, **kwargs):

        """ Copy self onto parent """

        kwargs.update({"order": self.order,
                       "rampup": self.ramp,
                       "duration": self.total_duration,
                       "temperature": self.temperature})

        return parent.add_step(**kwargs)

    @property
    def temperature(self):

        """ Return step temperature """

        return self.data['stepTemp']

    def __str__(self):

        return f"{ self.temperature } &deg;C"


class MashStep(StepMixin, api.Step):

    """ Step wrapper """

    def __init__(self, data):

        self.data = data

    @property
    def duration(self):

        return Duration(f"{ self.data['stepTime'] }m")

    @property
    def ramp(self):

        try:
            return Duration(f"{ self.data['ramp'] }m")
        except KeyError:
            return Duration("0m")

    @property
    def total_duration(self):

        """ For Brewfather mash steps, total time is time + ramp """

        return self.duration + self.ramp


BoilStep = MashStep


class FermentationStep(StepMixin, api.Step):

    """ Step wrapper for fermentation """

    def __init__(self, data):

        self.data = data

    def __str__(self):

        return self.data['type']

    @property
    def duration(self):

        return Duration(f"{ self.data['stepTime'] }d")

    @property
    def ramp(self):

        try:
            return Duration(f"{ self.data['ramp'] }d")
        except KeyError:
            return Duration("0m")

    @property
    def total_duration(self):

        """ For Brewfather mash steps, total time is time + ramp """

        return self.duration + self.ramp
