""" BrewFather resource """

from ninkasi.resource import Resource, ResourceRegistry
from .api import list_recipes, get_recipe, list_batches, get_batch
from .recipe import Recipe
from .batch import Batch


class RecipeResource(Resource):

    """ BrewFather resource. Call API and wrap results into Recipe
    class. """

    def list(self):

        return [Recipe(data) for data in list_recipes()]

    def get(self, _id):

        """ Wrap data in Recipe class """

        return Recipe(get_recipe(_id))


class BatchResource(Resource):

    """ Brewfather batches """

    def list(self):

        return [Batch(data) for data in list_batches()]

    def get(self, _id):

        """ Wrap data in Batch class """

        return Batch(get_batch(_id))
