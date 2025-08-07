""" Hopslist API """

import re
import requests
from bs4 import BeautifulSoup
from django.conf import settings
from ninkasi.utils import cache
from ninkasi.api import APIConnectionException
from .hop import Hop


BASE_URL = "https://www.hopslist.com/hops/"


ALPHANUMERIC_ONLY = re.compile(r"[^a-zA-Z0-9\s\-]")


def _call(url):

    """ Generic call """

    try:
        return requests.get(url, timeout=10)
    except requests.exceptions.ConnectionError as exc:
        raise APIConnectionException from exc


def table_with_alpha_acid(tag):

    """The Hopslist detail pages are somewhat erratic, so we need to
    find the table that has a header with 'Alpha Acid Composition'

    """

    return tag.name == "table" and tag.find(string="Alpha Acid Composition")


def list_hops():

    """ Get all hops from Hopslist """

    response = _call(BASE_URL)

    soup = BeautifulSoup(response.text, 'html.parser')

    for hop in soup.find_all("li", class_="listing-item"):

        name = ALPHANUMERIC_ONLY.sub('', hop.a.contents[0])

        yield Hop({'name': name, 'url': hop.a.attrs['href']})


@cache(time=3600)
def get_hop(_id):

    """ Get one hop. Sadly the hops hold diverse URL's, so we need to
    get the list in any case. """

    for hop in list_hops():

        if hop.id == _id:

            break

    response = _call(hop.data['url'])

    soup = BeautifulSoup(response.text, 'html.parser')

    content = soup.article

    hop_title = ALPHANUMERIC_ONLY.sub('', content.h1.contents[0])

    hop_descr = []

    for p in content.find("div", class_="entry-content").find_all("p")[:2]:
        for part in p.strings:

            hop_descr.append(part)

    hop_descr = " ".join(hop_descr)

    props = {}

    table = content.find(table_with_alpha_acid)

    defaults = {'name': hop_title, 'description': hop_descr}

    if not table:
        return Hop(defaults)

    for prop in table.find_all("tr"):

        try:
            prop_name = prop.td.contents[0]
            prop_val = prop.find_all("td")[1].contents[0]

            if prop_name == "Substitutes":

                defaults['subs'] = [
                    Hop({'name': ALPHANUMERIC_ONLY.sub('', a.contents[0])})
                    for a in prop.find_all("a")]
            else:
                defaults[prop_name] = prop_val

        except IndexError:
            pass

    return Hop(defaults)
