from ninkasi.tanks import TankRegistry
from ..models.tank import Tank
from .base import ListingView


class TankListingView(ListingView):

    """ Override base listing to add tank vocab

    """

    model = Tank

    def tank_vocab(self):

        """ Fetch all possible tank types """

        for tank in TankRegistry.list_tanks():

            yield tank
