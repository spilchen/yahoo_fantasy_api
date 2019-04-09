#!/bin/python

import pytest


@pytest.fixture()
def sc():
    # For testing, we don't call out to Yahoo!  We just use a sample json file.
    # For that reason the OAuth2 session context can be None.
    yield None
