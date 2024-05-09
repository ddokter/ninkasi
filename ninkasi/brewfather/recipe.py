from django.conf import settings
from ninkasi.api import Recipe as BaseRecipe
from ninkasi.brewfather import api


BASE_URL = "https://web.brewfather.app/tabs/recipes/recipe/"


class Recipe(BaseRecipe):

    """ BrewFather recipe

    TODO: cache data
    """

    mode = "ro"
    _data = {}

    def __init__(self, data):

        self._data = data

    def __str__(self):

        return self.name

    @property
    def urn(self):

        return f"urn:bf:{ self.id }"

    @property
    def id(self):

        return self.data['_id']

    @property
    def name(self):

        return self.data['name']

    @property
    def volume(self):

        return self.data['batchSize']

    @property
    def data(self):

        """ Get data from BrewFather and store in memory.
        TODO: cache in a better way
        """

        if not getattr(self, "_data", None):

            self._data = api.get_recipe(self.bf_id)

        return self._data

    def list_fermentables(self):

        return self.data['fermentables']

    def get_processing_time(self, unit='d'):

        """ Return the total processing time for the recipe. This includes
        brew, fermentation, maturation, etc """

        total = settings.BF_PROCESSING_TIME_OFFSET

        total += self.data['boilTime']

        total += self.data['hopStandMinutes']

        total += self.get_mash_time()

        # recalc to days...
        #
        total = total / 60 / 24

        total += self.get_fermentation_time()

        return total

    def get_mash_time(self):

        """ Return total of all mash steps in minutes """

        total = 0

        mash = self.data["mash"]

        for step in mash['steps']:

            total += step['stepTime']

        return total

    def get_fermentation_time(self):

        """ Return total of all fermentation steps in days """

        total = 0

        ferm = self.data["fermentation"]

        for step in ferm['steps']:

            total += step['stepTime']

        return total

    def get_url(self, mode):

        if mode == 'view':

            return f"{ BASE_URL }{ self.data['_id'] }"

        return "#"
