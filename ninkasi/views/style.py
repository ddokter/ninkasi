from .base import ListingView
from ..models.style import Style
from ..resource import ResourceRegistry


class StyleListingView(ListingView):

    """ Override base listing to show all resources for styles

    """

    model = Style

    def list_items(self):

        """ Fetch all styles from all resources """

        styles = []

        for resource in ResourceRegistry.get_resources('style'):

            styles.extend(resource.list())

        return styles
