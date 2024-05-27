""" BrewFather resource """

import logging
from ninkasi.api import APIConnectionException
from ninkasi.resource import Resource, NotFoundInResource
from .api import list_recipes, get_recipe, list_batches, get_batch
from .recipe import Recipe
from .batch import Batch


LOGGER = logging.getLogger("ninkasi")


class RecipeResource(Resource):

    """ BrewFather resource. Call API and wrap results into Recipe
    class. """

    def list(self):

        try:
            return [Recipe(data) for data in list_recipes()]
        except APIConnectionException:
            LOGGER.exception("Couldn't get recipes from Brewfather")
            return []

    def get(self, _id):

        """ Wrap data in Recipe class """

        try:
            return Recipe(get_recipe(_id))
        except APIConnectionException:
            LOGGER.exception("Couldn't get recipe from Brewfather API")
            return None


class BatchResource(Resource):

    """ Brewfather batches """

    def list(self):

        return [Batch(data) for data in list_batches()]

    def get(self, _id):

        """ Wrap data in Batch class """

        return Batch(get_batch(_id))
