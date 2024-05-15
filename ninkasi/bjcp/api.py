from gql import gql, Client
from gql.transport.aiohttp import AIOHTTPTransport
from aiohttp.client_exceptions import ClientConnectorError
from gql.transport.exceptions import TransportServerError
from django.conf import settings
from ninkasi.api import APIConnectionException
from ninkasi.utils import cache


LIST_STYLES_QRY = """query getAllBeerStyles {
    beerStyles(%PARAMS) {
    data {
    id
      attributes {
        reference
        name,
        overallImpression,
        aroma,
        appearance,
        flavor,
        mouthfeel,
        comments,
        entryInstructions,
        history,
        characteristicIngredients,
        styleComparison,
        vitalStatistics
        shortDescription
        ibuMin
        ibuMax
        fgMin
        fgMax
        ogMin
        ogMax
        srmMin
        srmMax
        abvMin
        abvMax
        style_tag_references {
         data {
           id
           attributes {
            tag
            description
           }
          }
        }
    }
  }
}
}
"""


def _call(qry):

    """ Call API with the given query and return the JSON result """

    # Select your transport with a defined url endpoint
    transport = AIOHTTPTransport(url=settings.BJCP_API_URL)

    # Create a GraphQL client using the defined transport
    client = Client(transport=transport, fetch_schema_from_transport=False)

    query = gql(qry)

    # Execute the query on the transport
    return client.execute(query)


@cache(time=3600)
def list_styles():

    """ Return listing of style definitions """

    try:
        return _call(LIST_STYLES_QRY.replace('%PARAMS', 'sort: "id"'))
    except (ClientConnectorError, TransportServerError) as exc:
        raise APIConnectionException from exc


@cache(time=3600)
def get_style(_id):

    """ Show one style """

    try:
        return _call(LIST_STYLES_QRY.replace(
            '%PARAMS', f'filters: {{ id: {{ eq: { _id } }} }}'))
    except (ClientConnectorError, TransportServerError) as exc:
        raise APIConnectionException from exc
