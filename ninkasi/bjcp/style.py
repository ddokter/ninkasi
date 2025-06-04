""" BJCP style implementation """

from django.conf import settings
from django.urls import reverse
from ninkasi.api import Style as BaseStyle
from ninkasi.bjcp import api


NID = "bjcp"


class Style(BaseStyle):

    """ Style class to wrap BJCP api style """

    source = NID
    _data = {}
    mode = "ro"

    def get_url(self, mode):

        if mode == 'view':

            return reverse('bjcp_view_style', kwargs={'pk': self.id})

        return "#"
    
    def __init__(self, data):

        self.data = data

    def __str__(self):

        return self.name

    @property
    def urn(self):

        return f"urn:{ NID }:{ self.id }"

    @property
    def id(self):

        return self.data['number']

    @property
    def name(self):

        return self.data['name']

    @property
    def color(self):

        if 'srmmin' in self.data and 'srmmax' in self.data:
            return f"{ self.data['srmmin'] },{ self.data['srmmax'] }"
        else:
            return "Unknown"
