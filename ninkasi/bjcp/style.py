""" BJCP style implementation """

from django.conf import settings
from ninkasi.api import Style as BaseStyle
from ninkasi.bjcp import api


NID = "bjcp"


class Style(BaseStyle):

    """ Style class to wrap BJCP api style """

    source = NID
    _data = {}
    mode = "ro"

    def __init__(self, data):

        self._data = data

    def __str__(self):

        return self.name

    @property
    def urn(self):

        return f"urn:{ NID }:{ self.id }"

    @property
    def id(self):

        return self.data['id']

    @property
    def name(self):

        return self.data['name']

    @property
    def color(self):

        return f"{ self.data['srmMin'] },{ self.data['srmMax'] }"

    @property
    def data(self):

        """ Get data from BrewFather and store in memory.
        TODO: cache in a better way
        """

        if not getattr(self, "_data", None):

            self._data = api.get_style(self.id)

        return self._data
