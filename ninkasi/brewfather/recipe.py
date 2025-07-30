from itertools import chain
from django.apps import apps
from django.conf import settings
from django.urls import reverse
from ninkasi.api import Recipe as BaseRecipe
from ninkasi.duration import Duration
from .phase import (Phase, MashStep, FermentationStep, BoilStep, FilterStep,
                    WhirlpoolStep)
from .ingredient import Ingredient


BASE_URL = "https://web.brewfather.app/tabs/recipes/recipe/"


class Recipe(BaseRecipe):

    """ BrewFather recipe

    TODO: cache data
    """

    mode = "ro"

    def __init__(self, data):

        self.data = data

    def __str__(self):

        return self.name

    @property
    def urn(self):

        return f"urn:bf:{self.id}"

    @property
    def id(self):

        return self.data['_id']

    @property
    def name(self):

        return self.data['name']

    @property
    def volume(self):

        return self.data['batchSize']

    def list_phases(self):

        """BF only provides data on mash, boil and fermentation, so
        other phases we'll add on defaults

        """

        phases = []

        phase = Phase("mash")

        for step in self.list_mash_steps():

            phase.add_step(step)

        phases.append(phase)

        phase = Phase("filter")

        phase.add_step(FilterStep(
            name="Circulate",
            temperature=80,
            duration=Duration("10m")
        ))

        phase.add_step(FilterStep(
            name="Filter",
            temperature=80,
            duration=Duration(settings.BF_FILTER_TIME)
        ))

        phase.add_step(FilterStep(
            name="Sparge",
            temperature=80,
            duration=Duration(settings.BF_SPARGE_TIME)
        ))

        phases.append(phase)

        phase = Phase("boil")

        phase.add_step(BoilStep({'stepTime': self.data['boilTime'],
                                 'stepTemp': 100}))

        phases.append(phase)

        phase = Phase("whirlpool")

        phase.add_step(WhirlpoolStep(
            name="Whirlpool",
            temperature=70,
            duration=Duration("10m")
        ))

        phases.append(phase)

        phase = Phase("fermentation")

        for step in self.list_fermentation_steps():

            phase.add_step(step)

        phases.append(phase)

        return phases

    def list_malts(self):

        """ List ingredients that are fermentable according to BF """

        Unit = apps.get_model("ninkasi", "Unit")

        unit = Unit.objects.get(name="Kilo")

        for fermentable in self.data['fermentables']:

            if fermentable['type'] == "Grain":
                yield Ingredient(data={'name': fermentable['name'],
                                       'type': fermentable['type'],
                                       'itype': 'malt',
                                       'percentage': fermentable['percentage'],
                                       'amount': fermentable['amount'],
                                       'unit': unit})

    def list_hops(self):

        Unit = apps.get_model("ninkasi", "Unit")

        unit = Unit.objects.get(name="Gram")

        for hop in self.data['hops']:
            yield Ingredient(data={'name': hop['name'],
                                   'type': hop['type'],
                                   'itype': 'hop',
                                   'amount': hop['amount'],
                                   'unit': unit})

    def list_yeasts(self):

        for yeast in self.data['yeasts']:
            yield Ingredient(data={'name': yeast['name'],
                                   'itype': 'yeast',
                                   'type': yeast['type'],
                                   'amount': yeast['amount'],
                                   'unit': yeast['unit']})

    def list_other(self):

        Unit = apps.get_model("ninkasi", "Unit")

        unit = Unit.objects.get(name="Gram")

        for fermentable in self.data['fermentables']:

            if fermentable['type'] != "Grain":
                yield Ingredient(data={'name': fermentable['name'],
                                       'type': fermentable['type'],
                                       'itype': 'malt',
                                       'amount': fermentable['amount'],
                                       'unit': unit})

        for misc in self.data['miscs']:
            yield Ingredient(data={'name': misc['name'],
                                   'type': misc['type'],
                                   'itype': 'misc',
                                   'amount': misc['amount'],
                                   'unit': unit})

    def list_ingredients(self):

        """ List materials for this recipe as a list of 'Ingredient' objects.

        TODO: add yeast and misc; get Kilo from settings?
        TODO: get unit in a more secure way
        """

        return chain(self.list_fermentables(), self.list_hops(),
                     self.list_yeasts())

    def get_total_duration(self):

        """ Return the total processing time for the recipe. This includes
        brew, fermentation, maturation, etc """

        total = settings.BF_PROCESSING_TIME_OFFSET

        total += self.data['boilTime']

        total += self.data['hopStandMinutes']

        duration = self.get_mash_time()
        duration += self.get_fermentation_time()

        duration += Duration(f"{total}m")

        return duration

    def get_mash_time(self):

        """ Return total of all mash steps in minutes """

        return sum(step.duration for step in self.list_mash_steps())

    def list_mash_steps(self):

        """ Return all mash steps """

        mash = self.data["mash"]

        for step in mash['steps']:

            yield MashStep(step)

    def list_fermentation_steps(self):

        """ Return all fermentation steps """

        phase = self.data["fermentation"]

        for step in phase['steps']:

            yield FermentationStep(step)

    def get_fermentation_time(self):

        """ Return total of all fermentation steps in days """

        return sum(step.duration for step in self.list_fermentation_steps())

    def get_url(self, mode):

        if mode == 'view':

            return reverse('brewfather_view_recipe', kwargs={'pk': self.id})

        return "#"

    def get_milestone_value(self, milestone, quantity):

        if milestone == "ninkasi.brew.end":
            if quantity.name == "volume":
                return self.volume

        return None
