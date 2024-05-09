""" BrewFather resource """

from ninkasi.resource import Resource, ResourceRegistry
from .api import list_recipes, get_recipe
from .recipe import Recipe


class RecipeResource(Resource):

    """ BrewFather resource. Call API and wrap results into Recipe
    class. """

    def list(self):

        return [Recipe(data) for data in list_recipes()]

    def get(self, _id):

        """ Wrap data in Recipe class """

        return Recipe(get_recipe(_id))
