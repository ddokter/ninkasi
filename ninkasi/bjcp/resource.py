""" BrewFather resource """

import logging
from ninkasi.resource import Resource
from ninkasi.api import APIConnectionException
from .api import list_styles, get_style
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

        """ return one single  style by the given BJCP id """

        try:
            style = get_style(_id)['beerStyles']['data'][0]

            data = style['attributes']
            data['id'] = style['id']

            return Style(data)
        except APIConnectionException:
            LOGGER.exception("Couldn't get style from BJCP API")
            return None
