from django.urls import reverse
from ninkasi.api import Hop as BaseHop


def str2range(val):

    """ Convert string to range """

    return val.replace('-', ',').replace('%', '')


# Map hop from hopslist to Hop model, using converter.
#
PROP_MAPPING = {
    "alpha_acid": ("Alpha Acid Composition", str2range),
    "beta_acid": ("Beta Acid Composition", str2range),
}


class Hop(BaseHop):

    """ Hopslist hop
    """

    mode = "ro"

    def __init__(self, data):

        self.data = data

    def __str__(self):

        return self.name

    @property
    def urn(self):

        return f"urn:hopslist:{self.id}"

    @property
    def id(self):

        return self.name.lower().replace(' ', '-')

    def get_url(self, mode):

        if mode == 'view':

            return reverse('hopslist_view_hop', kwargs={'pk': self.id})

        return "#"

    @property
    def alpha_acid(self):
        key, converter = PROP_MAPPING['alpha_acid']
        return converter(self.data[key])

    @property
    def beta_acid(self):
        key, converter = PROP_MAPPING['beta_acid']
        return converter(self.data[key])

    def __getattr__(self, name):

        if name not in self.data:
            return super().__getattr__(name)

        return self.data[name]
