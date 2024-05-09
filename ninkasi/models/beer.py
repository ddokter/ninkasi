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
    can be further linked to a recipe, but it is not the same.

    TODO: make recipe multiple field
    """

    name = models.CharField(_("Name"), max_length=100)
    style = URNField(max_length=100, registry='style', choices=list_styles)
    recipe = URNField(max_length=100, registry='recipe', choices=list_recipes)
    description = models.TextField()

    recipes = URNListField(null=True, blank=True, registry='recipe',
                           choices=list_recipes)

    def get_processing_time(self):

        """Return the processing time for this beer, provided as a
        Duration object.

        """

        try:
            return self.get_recipe().get_total_duration()
        except AttributeError:
            return settings.DEFAULT_PROCESSING_TIME

    def __str__(self):

        return f"{ self.name } ({ self.style })"

    def list_batches(self):

        """ All batches for this beer """

        return self.batch_set.all()

    def get_style(self):

        """Fetch the style for the beer. This should be a generally
        recognized style, i.e. BJCP or other.

        """

        nid = self._meta.get_field("style").get_ns(self.style)
        _id = self._meta.get_field("style").get_id(self.style)

        res = ResourceRegistry.get_resource('style', nid)

        return res.get(_id)

    def get_recipe(self):

        """ Fetch the actual recipe
        TODO: leave this to the field itself
        """

        nid = self._meta.get_field("recipe").get_ns(self.style)
        _id = self._meta.get_field("recipe").get_id(self.style)

        res = ResourceRegistry.get_resource('recipe', nid)

        return res.get(_id)

    class Meta:

        app_label = "ninkasi"
        ordering = ["name"]
