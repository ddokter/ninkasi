from math import ceil
from django.db import models
from django.utils.translation import gettext_lazy as _
from django.contrib.contenttypes.fields import GenericRelation
from .unit import Unit
from .ingredient import Ingredient
from .step import Step


class Recipe(models.Model):

    """ Brew recipe for a given beer, including ingredients, mash and
    fermentation profiles, etc."""

    name = models.CharField(_("Name"), max_length=100)
    descr = models.CharField(_("Description"), max_length=200, null=True,
                             blank=True)
    volume = models.SmallIntegerField(_("Volume"))
    ingredient = models.ManyToManyField(Ingredient, through="RecipeIngredient")
    step = GenericRelation(Step)

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

    def list_batches(self):

        """ Return list of batches related to this recipe """

        return self.batch_set.all()

    def list_steps(self):

        """ return both brewing steps and fermentation steps """

        return self.step.all()
        
    def get_total_duration(self, unit='day'):

        """ TODO: use days or no """

        return ceil(sum([step.get_duration() for step in self.step.all()]) /
                    (60 * 24))

    class Meta:
        ordering = ["name"]
        app_label = "ninkasi"
        verbose_name = _("Recipe")
        verbose_name_plural = _("Recipes")


class RecipeIngredient(models.Model):

    # TODO: make sure that there is a conversion from given unit to
    # ingredient's default unit

    amount = models.FloatField(_("Amount"))
    unit = models.ForeignKey(Unit, on_delete=models.CASCADE)
    recipe = models.ForeignKey(Recipe, on_delete=models.CASCADE)
    ingredient = models.ForeignKey(Ingredient, on_delete=models.CASCADE)


    @property
    def label(self):

        return _("Ingredients")

    def __str__(self):

        return "%s %s" % (self.ingredient, self.amount)
