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


# Map hop from hopslist to Hop model, using converter.
#
PROP_MAPPING = {
    "Alpha Acid Composition": ["alpha_acid", str2range],
    "Beta Acid Composition": ["beta_acid", str2range],
}


SUBS = {}


class Command(BaseCommand):

    def handle(self, *args, **options):

        if options['verbosity'] > 1:
            self.stdout.write("Calling Hopslist")

        hops = []

        response = requests.get(BASE_URL)

        soup = BeautifulSoup(response.text, 'html.parser')

        # print(soup.prettify())

        for hop in soup.find_all("li", class_="listing-item")[:5]:

            try:
                self.handle_hop(hop.a.attrs['href'], options)
            except IndexError:
                print(f"Problem handling {hop}")

        # Now that all hops are there, create substitute listings
        #
        self.handle_subs(options)

    def handle_hop(self, href, options):

        """ Handle one single hop """

        response = requests.get(href)

        soup = BeautifulSoup(response.text, 'html.parser')

        content = soup.article

        hop_title = content.h1.contents[0]

        if options['verbosity'] > 1:
            print(f"Handling hop {hop_title}")

        hop_descr = []

        for p in content.find("div", class_="entry-content").find_all("p")[:2]:
            for part in p.strings:

                hop_descr.append(part)

        hop_descr = " ".join(hop_descr)

        props = {}

        table = content.find("table", attrs={"width": "620"})

        if not table:
            return False

        defaults = {'name': hop_title, 'description': hop_descr}

        for prop in table.find_all("tr"):

            try:
                prop_name = prop.td.contents[0]
                prop_val = prop.find_all("td")[1].contents[0]

                if prop_name in PROP_MAPPING:

                    key, converter = PROP_MAPPING[prop_name]

                    defaults[key] = converter(prop_val)

                elif prop_name == "Substitutes":

                    SUBS[hop_title] = [a.contents[0] for
                                       a in prop.find_all("a")]
            except IndexError:
                pass

        return Hop.objects.update_or_create(defaults=defaults, name=hop_title)

    def handle_subs(self, options):

        """ Handle hop alternatives """

        for hop_name in SUBS:

            if options['verbosity'] > 1:
                print(f"Handling subs for {hop_name}")

            if Hop.objects.filter(name=hop_name).exists():

                hop = Hop.objects.get(name=hop_name)

                for sub_name in SUBS[hop_name]:

                    try:
                        if options['verbosity'] > 1:
                            print(f"  Found sub {sub_name}")
                        hop.substitutes.add(Hop.objects.get(name=sub_name))
                    except Hop.DoesNotExist:
                        print(f"Substitute {sub_name} not found")
