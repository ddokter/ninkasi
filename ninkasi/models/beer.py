from django.db import models
from django.utils.translation import gettext_lazy as _
from django.conf import settings
from ninkasi.resource import ResourceRegistry
from .fields import URNField, URNListField


def list_recipes():

    """List all recipes from all resources that provide them"""

    recipes = []

    for res in ResourceRegistry.get_resources("recipe"):
        recipes.extend((recipe.urn, recipe.name) for recipe in res.list())

    return recipes


def list_styles():

    """ List all styles from all resources """

    styles = []

    for res in ResourceRegistry.get_resources("style"):
        styles.extend((style.urn, style.name) for style in res.list())

    return styles


class Beer(models.Model):

    """A beer is defined by it's name, style and description. A beer
    can be further linked to one or more recipes.
    """

    name = models.CharField(_("Name"), max_length=100)
    style = URNField(max_length=100, registry='style', choices=list_styles)
    description = models.TextField()

    recipes = URNListField(null=True, blank=True, registry='recipe',
                           choices=list_recipes)

    def get_recipe(self, _id):

        """ Return the recipe by it's id. """

        for recipe in self.recipes:
            if recipe.id == _id:
                return recipe

        return None

    def __str__(self):

        return f"{ self.name } ({ self.style })"

    def list_batches(self):

        """ All batches for this beer """

        return self.batch_set.all()

    class Meta:

        app_label = "ninkasi"
        ordering = ["name"]
