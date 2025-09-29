from django.urls import reverse


def str2range(val):

    """ Convert string to range """

    return val.replace('-', ',').replace('%', '')


# Map hop from hopslist to Hop model, using converter.
#
PROP_MAPPING = {
    "alpha_acid": ("Alpha Acid Composition", str2range),
    "beta_acid": ("Beta Acid Composition", str2range),
}


class Hop():

    """ Hopslist hop
    """

    mode = "ro"

    def __init__(self, data):

        self.data = data

    def __str__(self):

        return self.data['name']

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

        return str2range(self.data['Alpha Acid Composition'])

    @property
    def beta_acid(self):

        return str2range(self.data['Beta Acid Composition'])

    def __getattr__(self, name):

        return super().__getattribute__('data')[name]

    def save(self, **kwargs):

        pass

    def delete(self, **kwargs):

        pass

    class Meta:

        managed = False
