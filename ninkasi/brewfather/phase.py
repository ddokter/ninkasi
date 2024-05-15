""" Brewfather implementatins for phase and steps """

from ninkasi import api
from ninkasi.duration import Duration


class Phase(api.Phase):

    """ Brewfather implementation of phase """

    def __init__(self, metaphase):

        self.metaphase = metaphase
        self.steps = []
        self.order = 0

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

    order = 0
    
    def copy(self, parent, **kwargs):

        """ Copy self onto parent """

        kwargs.update({"order": self.order,
                       "duration": self.total_duration,
                       "temperature": self.temperature})

        return self.__class__.objects.create(phase=parent, **kwargs)
    
    @property
    def temperature(self):

        return self.data['stepTemp']

class MashStep(api.Step):

    """ Step wrapper """

    def __init__(self, data):

        self.data = data

    @property
    def total_duration(self):

        """ For Brewfather mash steps, total time is time + ramp """

        duration = Duration(f"{ self.data['stepTime'] }m")

        if self.data['rampTime']:

            duration += Duration(f"{ self.data['rampTime'] }m")

        return duration


class FermentationStep(api.Step):

    """ Step wrapper for fermentation """

    def __init__(self, data):

        self.data = data

    def __str__(self):

        return self.data['type']

    @property
    def total_duration(self):

        """ For Brewfather mash steps, total time is time + ramp """

        duration = Duration(f"{ self.data['stepTime'] }d")

        if self.data.get('ramp', None):

            duration += Duration(f"{ self.data['ramp'] }d")

        return duration
