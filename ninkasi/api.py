""" API definitions for Ninkasi """

from django.apps import apps
from .ordered import OrderedContainer
from .registry import PhaseRegistry


class APIConnectionException(Exception):

    """ Whenever an API cannot be reached, this exception should be raised """


class Style:

    """Base style class, defining what Ninkasi expects of a
    beerstyle. All models must implement the methods described here.

    """

    @property
    def name(self):

        """ Return style name """

    @property
    def color(self):

        """ Return color range as tuple of int's """

    @property
    def urn(self):

        """ Style identifier """


class Recipe:

    """ Base recipe class, defining what Ninkasi expects of a recipe. All
    recipe models must implement the methods described here.
    """

    @property
    def urn(self):

        """ identifier """

    @property
    def volume(self):

        """ Return batch volume for this recipe """

    def list_phases(self):

        """ Return a list of BasePhase objects, ordered """


class Batch:

    """ Base batch class
    """

    @property
    def urn(self):

        """ identifier """

    @property
    def name(self):

        """ Return batch name """

    @property
    def volume(self):

        """ Return batch volume for this recipe """


class Phase(OrderedContainer):

    """Base class for defining phases. Extend this class for
    implementing any type of phase. Class must support deepcopy.

    """

    metaphase = None

    def list_steps(self, raw=False):

        """Return list of all steps for this phase. If raw is True do
        not look for actual implementation of the steps, given that a
        step may have different implementations.

        """

    def get_child_qs(self):

        return self.list_steps(raw=True)

    def copy(self, parent):

        """ Provide a deep copy of self onto parent """

    def __eq__(self, thing):

        """Determine whether the phases are equal. This needs to dig
        into any subs.

        """


class Step:

    """ Step in the process. Could be mash step, of fermentation step """

    def get_total_duration(self):

        """ Get total duration, including rampu up etc. """

    @property
    def name(self):

        """ step name """

    def copy(self, parent):

        """ Provide a copy of self onto parent """


class MetaPhase:

    """ Define phases that may be used throughout Ninkasi """

    steps = []

    @property
    def id(self):

        """ return the unique id """

    @property
    def name(self):

        """ Front end name """

    def list_step_models(self):

        """ return a list of step models that may be added to this phase """

        return self.steps

    def get_default_step_model(self):

        """ Get the step model for this meta """

        parts = self.steps[0].split(".")

        return apps.get_model(parts[0], parts[1])


class MashMetaPhase(MetaPhase):

    """ Mash for any brew """

    id = "mash"
    name = "Mash"
    parents = ["brew", "recipe"]
    steps = ["ninkasi.MashStep", "ninkasi.Step"]


class BoilMetaPhase(MetaPhase):

    """ Boil for any brew. Could be absent for raw ales. """

    id = "boil"
    name = "Boil"
    parents = ["brew", "recipe"]
    steps = ["ninkasi.BoilStep", "ninkasi.Step"]


class MaturationMetaPhase(MetaPhase):

    """ Maturation, that is the stage after fermentation """

    id = "maturation"
    name = "Maturation"
    parents = ["batch", "recipe"]
    steps = ["ninkasi.MaturationStep"]


class FermentationMetaPhase(MetaPhase):

    """All fermentation steps. For Ninkasi, this does not include
    maturation etc., purely actual yeast fermentation.

    """

    id = "fermentation"
    name = "Fermentation"
    parents = ["batch", "recipe"]
    steps = ["ninkasi.FermentationStep"]


class PackagingMetaPhase(MetaPhase):

    """ Packaging, i.e. bottling and kegging. """

    id = "packaging"
    name = "Packaging"
    parents = ["batch"]
    steps = ["ninkasi.PackagingStep"]
