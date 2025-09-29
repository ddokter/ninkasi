""" Recipe model and related stuff """

from math import ceil
from django.db import models
from django.apps import apps
from django.utils.translation import gettext_lazy as _
from django.contrib.contenttypes.fields import GenericRelation
from django.contrib.contenttypes.models import ContentType
from django.conf import settings
from ninkasi.resource import Resource, ResourceRegistry, NotFoundInResource
from ..api import Recipe as BaseRecipe
from .unit import Unit
from .ingredient import Ingredient
from ..ordered import OrderedContainer
from .malt import Malt
from .hop import Hop
from .yeast import Yeast
from .other import Other
from .phase import PhaseIngredient


class Recipe(models.Model, BaseRecipe, OrderedContainer):

    """Brew recipe for a given beer, including ingredients, processing
    aids, mash and fermentation profiles, etc.  The Recipe is also an
    ordered container for it's phases.

    A recipe is related to one brewhouse, since that determines
    amounts of ingredients. It is also related to a Beer

    """

    brewhouse = models.ForeignKey("Brewhouse", on_delete=models.CASCADE)
    beer = models.ForeignKey("Beer", on_delete=models.CASCADE)

    name = models.CharField(_("Name"), max_length=100)
    volume = models.SmallIntegerField(_("Volume"))
    ingredient = models.ManyToManyField(Ingredient, through="RecipeIngredient")

    phase = GenericRelation("Phase")

    def __str__(self):

        return self.name

    def list_ingredients(self, clazz=None):

        qry = PhaseIngredient.objects.filter(phase__in=self.list_phases())

        for res in qry:
            if res.ingredient.get_real().__class__ == clazz:
                yield res

    def list_malts(self):

        """ List all malt ingredients """

        return self.list_ingredients(clazz=Malt)

    def list_hops(self):

        """ List all malt ingredients """

        return self.list_ingredients(clazz=Hop)

    def list_yeasts(self):

        """ List all malt ingredients """

        return self.list_ingredients(clazz=Yeast)

    def list_other(self):

        """ List all malt ingredients """

        return self.list_ingredients(clazz=Other)

    def get_grist_weight(self):

        raise NotImplementedError

    def list_steps(self):

        """ return both brewing steps and fermentation steps """

        return []

    def list_phases(self):

        """ return both brewing steps and fermentation steps """

        return self.phase.all()

    def add_phase(self, metaphase):

        """ Add phase of the metpahase given """

        self.phase.create(metaphase=metaphase, order=self.phase.count())

    def get_total_duration(self):

        """ TODO: use days or no """

        return sum(phase.get_duration() for phase in self.list_phases())

    def get_milestone_value(self, milestone, quantity):

        evt_map = {
            ('ninkasi.brew.end', 'volume'): self.volume,
            ('ninkasi.brew.end', 'gravity'): self.original_gravity
        }

        return evt_map.get((milestone, quantity), None)

    class Meta:

        """This model is swappable, by the value of RECIPE_MODEL in
        settings

        """

        app_label = "ninkasi"
        verbose_name = _("Recipe")
        verbose_name_plural = _("Recipes")


class RecipeIngredient(models.Model):

    """Ingredients are related to a recipe with a given amount, but
    also a time to add. This allows for hop gifts to be specified, but
    also for example steeping malts.

    """

    # TODO: make sure that there is a conversion from given unit to
    # ingredient's default unit

    amount = models.FloatField(_("Amount"))
    unit = models.ForeignKey(Unit, on_delete=models.CASCADE)
    recipe = models.ForeignKey("Recipe", on_delete=models.CASCADE)
    addition_time = models.FloatField(blank=True, null=True)
    ingredient = models.ForeignKey(Ingredient, on_delete=models.CASCADE)

    @property
    def name(self):

        return self.ingredient.name

    def __str__(self):

        return f"{self.ingredient} {self.amount}"
