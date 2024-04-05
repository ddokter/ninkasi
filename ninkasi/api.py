""" API definitions for Ninkasi """


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
