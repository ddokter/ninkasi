from django.core.management.base import BaseCommand
from django.conf import settings
from bs4 import BeautifulSoup
import requests
from ninkasi.models.hop import Hop


HELP = """Hopslist listing
Usage: hopslist
"""

BASE_URL = "https://www.hopslist.com/hops/"


def str2range(val):

    """ Convert string to range """

    return val.replace('-', ',').replace('%', '')


PROP_MAPPING = {
    "Alpha Acid Composition": ["alpha_acid", str2range]
}


class Command(BaseCommand):

    def handle(self, *args, **options):

        if options['verbosity'] > 1:
            self.stdout.write("Calling Hopslist")

        hops = []

        response = requests.get(BASE_URL)

        soup = BeautifulSoup(response.text, 'html.parser')

        # print(soup.prettify())

        for hop in soup.find_all("li", class_="listing-item"):

            hops.append(hop.a.attrs['href'])

        self.handle_hop(hops[0])

    def handle_hop(self, href):

        """ Handle one single hop """

        response = requests.get(href)

        soup = BeautifulSoup(response.text, 'html.parser')

        content = soup.article

        hop_title = content.h1.contents[0]

        hop_descr = []

        for p in content.find("div", class_="entry-content").find_all("p")[:2]:
            for part in p.strings:

                hop_descr.append(part)

        hop_descr = " ".join(hop_descr)

        props = {}

        for prop in content.find_all("table")[1].find_all("tr"):

            try:
                props[prop.td.contents[0]] = prop.find_all("td")[1].contents[0]
            except IndexError:
                pass

        defaults = {'name': hop_title, 'description': hop_descr}

        for prop in props:
            if prop in PROP_MAPPING:

                key, converter = PROP_MAPPING[prop]

                defaults[key] = converter(props[prop])

        Hop.objects.update_or_create(defaults=defaults, name=hop_title)
