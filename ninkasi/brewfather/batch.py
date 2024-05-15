from django.conf import settings
from ninkasi.api import Recipe as BaseRecipe
from ninkasi.api import Batch as BaseBatch
from ninkasi.brewfather import api


BASE_URL = "https://web.brewfather.app/tabs/batches/batch/"


class Batch(BaseBatch):

    """ BrewFather batch

    TODO: cache data
    """

    mode = "ro"
    _data = {}

    def __init__(self, data):

        self._data = data

    def __str__(self):

        return self.name

    @property
    def urn(self):

        return f"urn:bf:{ self.id }"

    @property
    def id(self):

        return self.data['_id']

    @property
    def name(self):

        return self.data['name']

    @property
    def volume(self):

        return self.data['batchSize']

    @property
    def data(self):

        """ Get data from BrewFather and store in memory.
        TODO: cache in a better way
        """

        if not getattr(self, "_data", None):

            self._data = api.get_batch(self.bf_id)

        return self._data

    def get_url(self, mode):

        """ Remote URL """

        if mode == 'view':

            return f"{ BASE_URL }{ self.data['_id'] }"

        return "#"
