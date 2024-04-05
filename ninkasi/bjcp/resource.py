""" BrewFather resource """

import logging
from ninkasi.resource import Resource, ResourceRegistry
from ninkasi.api import APIConnectionException
from .api import list_styles
from .style import Style


LOGGER = logging.getLogger("ninkasi")


class StyleResource(Resource):

    """BJCP resource using the BJCP api. Call API and wrap results
    into ninkasi.api.Style implementation class.

    """

    def list(self):

        """ List styles from BJCP api as bjcp.Style objects """

        styles = []

        try:
            for style in list_styles()['beerStyles']['data']:

                data = style['attributes']
                data['id'] = style['id']

                styles.append(Style(data))
        except APIConnectionException:
            LOGGER.exception("Couldn't get styles from BJCP API")
            
        return styles

    def get(self, _id):

        """ return get_recipe(_id) """

        return {'name': 'foo', 'id': _id, 'source': 'bjcp'}
