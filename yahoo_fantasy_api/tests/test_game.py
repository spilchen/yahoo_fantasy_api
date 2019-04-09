#!/bin/python

from yahoo_fantasy_api import game, league
import mock_yhandler

# For testing, we don't call out to Yahoo!  We just use a sample json file.
# For that reason the OAuth2 session context can be None.
TEST_SESSION_CONTEXT = None


def test_ids():
    gm = game.Game(TEST_SESSION_CONTEXT, 'mlb')
    gm.inject_yhandler(mock_yhandler.YHandler())
    ids = gm.league_ids()
    for i in ids:
        print(i)
    assert(len(ids) == 12)
    print(ids)
    assert(ids[5] == '268.l.46645')


def test_ids_for_year():
    gm = game.Game(TEST_SESSION_CONTEXT, 'mlb')
    gm.inject_yhandler(mock_yhandler.YHandler())
    ids = gm.league_ids(year=2017)
    assert(len(ids) == 1)
    print(ids)
    assert(ids[0] == '370.l.56877')


def test_to_league():
    gm = game.Game(TEST_SESSION_CONTEXT, 'mlb')
    gm.inject_yhandler(mock_yhandler.YHandler())
    lg = gm.to_league('370.l.56877')
    assert(type(lg) is league.League)
