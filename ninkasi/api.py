""" Define API for Ninkasi """


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


class MashMetaPhase(MetaPhase):

    id = "mash"
    name = "Mash"
    steps = ["ninkasi.MashStep", "ninkasi.Step"] 


class MaturationMetaPhase(MetaPhase):

    id = "maturation"
    name = "Maturation"
    steps = ["ninkasi.MaturationStep"]


class FermentationMetaPhase(MetaPhase):

    id = "fermentation"
    name = "Fermentation"
    steps = ["ninkasi.FermentationStep"]
