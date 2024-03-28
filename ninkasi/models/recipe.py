""" Recipe model and related stuff """

from math import ceil
from django.db import models
from django.apps import apps
from django.utils.translation import gettext_lazy as _
from django.contrib.contenttypes.fields import GenericRelation
from django.conf import settings
from .unit import Unit
from .ingredient import Ingredient
from .step import RecipeStep


def get_recipe_model():

    """ Return the configured recipe model """

    module, model = settings.RECIPE_MODEL.split(".")

    return apps.get_model(module, model)


class AbstractRecipe(models.Model):

    """ Base recipe class, defining what Ninkasi expects of a recipe. All
    recipe models must implement the methods described here.
    """

    @property
    def volume(self):

        """ Return batch volume for this recipe """

    def list_phases(self):

        """ Return a list of BasePhase objects, ordered """

    class Meta:

        app_label = "ninkasi"
        abstract = True


class Recipe(AbstractRecipe):

    """Brew recipe for a given beer, including ingredients,
    processing aids, mash and fermentation profiles, etc.

    """

    name = models.CharField(_("Name"), max_length=100)
    volume = models.SmallIntegerField(_("Volume"))
    # ingredient = models.ManyToManyField(Ingredient, through="RecipeIngredient")

    def __str__(self):

        return self.name

    @property
    def has_ingredients(self):

        return self.recipeingredient_set.exists()

    def list_ingredients(self, _filter={}):

        """ List all ingredients, use filter if there """

        return self.recipeingredient_set.filter(**_filter).prefetch_related(
            "ingredient",
            "unit")

    def list_steps(self):

        """ return both brewing steps and fermentation steps """

        return []

    def list_phases(self):

        """ return both brewing steps and fermentation steps """

        return self.recipephase_set.all()    

    def get_total_duration(self, unit='day'):

        """ TODO: use days or no """

        return ceil(sum(phase.get_duration() for phase in self.list_phases()) /
                    (60 * 24))

    class Meta(AbstractRecipe.Meta):

        """This model is swappable, by the value of RECIPE_MODEL in
        settings

        """

        swappable = 'RECIPE_MODEL'
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
    recipe = models.ForeignKey(settings.RECIPE_MODEL, on_delete=models.CASCADE)
    ingredient = models.ForeignKey(Ingredient, on_delete=models.CASCADE)
    addition = models.ForeignKey("RecipeStep", on_delete=models.SET_NULL,
                                 blank=True, null=True)
    addition_time = models.FloatField(blank=True, null=True)

    def __str__(self):

        return f"{ self.ingredient } { self.amount }"
