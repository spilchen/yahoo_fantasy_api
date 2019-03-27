#!/bin/python

import json

YAHOO_ENDPOINT = 'https://fantasysports.yahooapis.com/fantasy/v2'


def get(sc, uri):
    """Send an API request to the URI and return the response as JSON

    Args:
        sc - OAuth2 session context
        uri - URI of the API to call

    Return:
        JSON document of the response
    """
    response = sc.session.get("{}/{}".format(YAHOO_ENDPOINT, uri),
                              params={'format': 'json'})
    jresp = response.json()
    if "error" in jresp:
        raise RuntimeError(json.dumps(jresp))
    return jresp
