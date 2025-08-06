from django.db import models
from django.db.models import Q
from django.utils.translation import gettext_lazy as _
from django.apps import apps
from .material import Material


class Ingredient(Material):

    """Specific material for beer, i.e. an ingredient that goes into
    the brew. The Ingredient model may be subclassed to specify the
    role of the ingredient in the brew. These are defined as: malt,
    hop, yeast or misc. Most brewing apps use 'fermentable', but for
    Ninkasi other fermentables than malt are categorized under misc.

    Ingredient is a class by itself, to distinguish between production
    aids, that do not need to be considered on a batch, given that
    they are not actually _in_ the beer.

    """

    def list_recipes(self):

        """ Return list of all recipes using this ingredient """

        ri_model = apps.get_model("ninkasi", "RecipeIngredient")
        recipe_model = apps.get_model("caboose", "Recipe")

        recipe_ids = ri_model.objects.filter(
            ingredient=self).values_list("recipe__id", flat=True)

        return recipe_model.objects.filter(id__in=recipe_ids)

    @property
    def categories(self):

        return [str(cat) for cat in self.category.all()]

    class Meta:
        app_label = "ninkasi"
        ordering = ["name"]
