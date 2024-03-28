""" Brewfather API """

import requests
from requests.auth import HTTPBasicAuth
from django.conf import settings


def _call(url):

    """ Generic call, setting the auth header """

    basic = HTTPBasicAuth(settings.BF_USER_ID, settings.BF_API_KEY)

    try:
        # return requests.get(url, auth=basic, timeout=10).json()
        return []
    except requests.exceptions.ConnectionError:
        return []


def list_fermentables():

    """ Get all fermentables from BrewFather """

    url = "https://api.brewfather.app/v2/inventory/fermentables"

    return _call(url)


def list_recipes():

    """ Get the recipes """

    return _call("https://api.brewfather.app/v2/recipes")

def get_recipe(_id):

    """ Get one recipe """

    return _call(f"https://api.brewfather.app/v2/recipes/{ _id }")
