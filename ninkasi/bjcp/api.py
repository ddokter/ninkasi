from pathlib import Path
import json
from django.conf import settings
from ninkasi.api import APIConnectionException
from ninkasi.utils import cache


def _call():

    """ Call API with the given query and return the JSON result """

    path = Path(__file__).with_name('styles.json')

    with path.open('r') as f:
        return json.load(f)


@cache(time=3600)
def list_styles():

    """ Return listing of style definitions """

    try:
        return _call()
    except:
        raise APIConnectionException


@cache(time=3600)
def get_style(_id):

    """ Show one style
    TODO: this is a tad dumbass.
    """

    try:
        for style in _call():
            if style['number'] == _id:
                return style
    except:
        raise APIConnectionException
