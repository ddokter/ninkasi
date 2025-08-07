""" BrewFather resource """

import logging
from ninkasi.api import APIConnectionException
from ninkasi.resource import Resource
from .api import list_hops, get_hop


LOGGER = logging.getLogger("ninkasi")


class HopResource(Resource):

    """Hoplist resource.

    """

    def list(self):

        try:
            return list_hops()
        except APIConnectionException:
            LOGGER.exception("Couldn't get recipes from Hopslist")
            return []

    def get(self, _id):

        """ Get one hop """

        try:
            return get_hop(_id)
        except APIConnectionException:
            LOGGER.exception("Couldn't get recipe from Hopslist API")
            return None
