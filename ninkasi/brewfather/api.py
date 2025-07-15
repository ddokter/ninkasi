""" Brewfather API """

import requests
from requests.auth import HTTPBasicAuth
from django.conf import settings
from ninkasi.utils import cache
from ninkasi.api import APIConnectionException


def _call(url):

    """ Generic call, setting the auth header """

    basic = HTTPBasicAuth(settings.BF_USER_ID, settings.BF_API_KEY)

    try:
        return requests.get(url, auth=basic, timeout=10).json()
    except requests.exceptions.ConnectionError as exc:
        raise APIConnectionException from exc


def list_fermentables(limit=50):

    """ Get all fermentables from BrewFather """

    if limit == -1:

        fermentables = []

        _id = None

        while True:
            url = (f"https://api.brewfather.app/v2/inventory/fermentables?"
                   f"limit=50&complete=True"
                   )

            if _id:
                url += f"&start_after={_id}"

            print(url)

            fermentables += _call(url)

            if _id == fermentables[-1]['_id']:
                break

            _id = fermentables[-1]['_id']

        return fermentables

    else:
        url = (f"https://api.brewfather.app/v2/inventory/fermentables?"
               f"limit={limit}&complete=True"
               )

        return _call(url)


@cache(time=3600)
def list_recipes():

    """ Get the recipes """

    return _call("https://api.brewfather.app/v2/recipes?limit=50")


@cache(time=3600)
def get_recipe(_id):

    """ Get one recipe """

    return _call(f"https://api.brewfather.app/v2/recipes/{_id}")


@cache(time=3600)
def list_batches():

    """ Get all batches from brewfather """

    return _call("https://api.brewfather.app/v2/batches")


@cache(time=3600)
def get_batch(_id):

    """ Get one batch """

    return _call(f"https://api.brewfather.app/v2/batches/{_id}")
