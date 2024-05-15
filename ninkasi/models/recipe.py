""" Recipe model and related stuff """

from math import ceil
from django.db import models
from django.apps import apps
from django.utils.translation import gettext_lazy as _
from django.contrib.contenttypes.fields import GenericRelation
from django.conf import settings
from ninkasi.resource import Resource, ResourceRegistry
from ..api import Recipe as BaseRecipe
from .unit import Unit
from .ingredient import Ingredient
from ..ordered import OrderedContainer


class RecipeResource(Resource):

    def list(self):

        return Recipe.objects.all()

    def get(self, _id):

        return Recipe.objects.get(pk=_id)


ResourceRegistry.register("recipe", "django", RecipeResource())


class Recipe(models.Model, BaseRecipe, OrderedContainer):

    """Brew recipe for a given beer, including ingredients,
    processing aids, mash and fermentation profiles, etc.

    """

    name = models.CharField(_("Name"), max_length=100)
    volume = models.SmallIntegerField(_("Volume"))
    # ingredient = models.ManyToManyField(Ingredient, through="RecipeIngredient"
    phase = GenericRelation("Phase")

    def get_child_qs(self):

        return self.phase
    
    def __str__(self):

        return self.name

    @property
    def urn(self):

        return f"urn:django:{ self.id }"

    @property
    def has_ingredients(self):

        return self.recipeingredient_set.exists()

    def list_ingredients(self, _filter={}):

        """ List all ingredients, use filter if there """

        return self.recipeingredient_set.filter(**_filter).prefetch_related(
            "ingredient",
            "unit")

    def list_fermentables(self):

        raise NotImplementedError

    def get_grist_weight(self):

        raise NotImplementedError
        
    def list_steps(self):

        """ return both brewing steps and fermentation steps """

        return []

    def list_phases(self):

        """ return both brewing steps and fermentation steps """

        return self.phase.all()

    def get_total_duration(self):

        """ TODO: use days or no """

        return sum(phase.get_duration() for phase in self.list_phases())

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
    also for example steeping malts

    """

    # TODO: make sure that there is a conversion from given unit to
    # ingredient's default unit

    amount = models.FloatField(_("Amount"))
    unit = models.ForeignKey(Unit, on_delete=models.CASCADE)
    recipe = models.ForeignKey("Recipe", on_delete=models.CASCADE)
    ingredient = models.ForeignKey(Ingredient, on_delete=models.CASCADE)
    addition = models.ForeignKey("RecipeStep", on_delete=models.SET_NULL,
                                 blank=True, null=True)
    addition_time = models.FloatField(blank=True, null=True)

    def __str__(self):

        return f"{ self.ingredient } { self.amount }"
