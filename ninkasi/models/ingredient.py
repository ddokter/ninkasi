from django.db import models
from django.db.models import Q
from django.utils.translation import gettext_lazy as _
from django.apps import apps
#from polymorphic.models import PolymorphicModel
from .category import Category
from .asset import Asset


class Ingredient(Asset):

    """ Specific asset for beer, i.e. an ingredient that goes into
    the brew. """
    
    def list_recipes(self):

        ri_model = apps.get_model("caboose", "RecipeIngredient")
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
