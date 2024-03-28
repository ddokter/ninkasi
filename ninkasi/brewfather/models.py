from django.db import models
from django.conf import settings
from ninkasi.models.recipe import AbstractRecipe
from ninkasi.brewfather import api


def recipe_vocab():

    """ List BrewFather recipes, for selection in proxy model """

    return [(recipe['_id'], recipe['name']) for recipe in api.list_recipes()]


class Recipe(AbstractRecipe):

    """ Brew recipe for a given beer, including ingredients, mash and
    fermentation profiles, etc. This recipe implementation gets data
    from BrewFather and links to a BF recie by it's ID.

    TODO: cache data
    """

    bf_id = models.CharField(max_length=100, choices=recipe_vocab)

    data = None

    def __str__(self):

        return self.name

    @property
    def name(self):

        return self.get_data()['name']

    @property
    def volume(self):

        return self.get_data()['batchSize']

    def get_data(self):

        """ Get data from BrewFather and store in memory.
        TODO: cache in a better way
        """

        if not getattr(self, "data", None):

            self.data = api.get_recipe(self.bf_id)

        return self.data

    def list_fermentables(self):

        data = self.get_data()

        return data['fermentables']

    def get_processing_time(self, unit='d'):

        """ Return the total processing time for the recipe. This includes
        brew, fermentation, maturation, etc """

        total = settings.BF_PROCESSING_TIME_OFFSET

        total += self.get_data()['boilTime']

        total += self.get_data()['hopStandMinutes']        

        total += self.get_mash_time()

        # recalc to days...
        #
        total = total / 60 / 24

        total += self.get_fermentation_time()

        return total

    def get_mash_time(self):

        """ Return total of all mash steps in minutes """

        total = 0

        mash = self.get_data()["mash"]

        for step in mash['steps']:

            total += step['stepTime']

        return total

    def get_fermentation_time(self):

        """ Return total of all fermentation steps in days """

        total = 0

        ferm = self.get_data()["fermentation"]

        for step in ferm['steps']:

            total += step['stepTime']

        return total



    class Meta(AbstractRecipe.Meta):

        app_label = "brewfather"
