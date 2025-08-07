from ninkasi.resource import ResourceRegistry
from .base import ListingView
from ..models.hop import Hop


class HopListingView(ListingView):

    """ Override base listing to show all resources for hops

    """

    model = Hop

    def list_items(self):

        """ Fetch all hops from all resources """

        hops = []

        for resource in ResourceRegistry.get_resources('hop'):

            hops.extend(resource.list())

        return hops
