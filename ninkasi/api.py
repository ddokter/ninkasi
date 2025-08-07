""" API definitions for Ninkasi """

from django.apps import apps
from .ordered import OrderedContainer


class APIConnectionException(Exception):

    """ Whenever an API cannot be reached, this exception should be raised """


class Base:

    """ Base class. Empty for now.
    """


class URNBase(Base):

    """Base classs for models that may have a remote data peer.  This
    can be used to define models within Ninkasi that really take their
    data from elsewhere, like BrewFather, etc.

    """

    @property
    def urn(self):

        """ Unique identifier, including protocol """


class Style(URNBase):

    """Base style class, defining what Ninkasi expects of a
    beerstyle. All models must implement the methods described here.

    """

    @property
    def name(self):

        """ Return style name """

    @property
    def color(self):

        """ Return color range as tuple of int's """


class Recipe(URNBase):

    """Base recipe class, defining what Ninkasi expects of a
    recipe. All recipe models must implement the methods described
    here. Other than most brewing apps, Ninkasi doesn't use
    'fermentables' as a ingredient category. It uses 'malts' and
    'other'.

    """

    INGREDIENT_CAT_MALT = 0
    INGREDIENT_CAT_HOP = 1
    INGREDIENT_CAT_YEAST = 2
    INGREDIENT_CAT_OTHER = 3

    @property
    def volume(self):

        """ Return volume for this recipe """

    def list_phases(self):

        """ Return a list of BasePhase objects, ordered """

    def list_malts(self):

        """ Return a list of all malts """

    def list_hops(self):

        """ Return a list of all hops """

    def list_yeasts(self):

        """ Return a list of yeasts """

    def list_other(self):

        """ Return a list of all 'other' ingredients """

    @property
    def final_gravity(self):

        """ Return final gravity in SG """

    @property
    def original_gravity(self):

        """ Return original gravity in SG """

    @property
    def ibu(self):

        """ Return bitterness in IBU """

    def get_milestone_value(self, milestone, quantity):

        """ Arguments must be milestone and Quantity object """


class Hop(URNBase):

    """ Hop may be remote """

    @property
    def alpha_acid(self):

        """ Essential feature for hops """

    @property
    def beta_acid(self):

        """ Secondary feature for hops """


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

    def get_duration(self):

        """ How lon is this step? Should return a Duration object. """

    def has_steps(self):

        """ Wel, do we? """

    def get_metaphase(self):

        """ Return asociated meta phase. Use get_model to prevent cirular
        imports, given that this api module is rather central. """

        model = apps.get_model("ninkasi", "MetaPhase")

        return model.objects.get(name__iexact=self.metaphase)

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

    """Define phases that may be used throughout Ninkasi. The phase
    consists of consecutive steps."""

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
