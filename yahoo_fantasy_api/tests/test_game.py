#!/bin/python

import yahoo_fantasy_api as yfa
import mock_yhandler


def test_ids(sc):
    gm = yfa.Game(sc, 'mlb')
    gm.inject_yhandler(mock_yhandler.YHandler())
    ids = gm.league_ids()
    for i in ids:
        print(i)
    assert(len(ids) == 12)
    print(ids)
    assert(ids[5] == '268.l.46645')


def test_ids_for_year(sc):
    gm = yfa.Game(sc, 'mlb')
    gm.inject_yhandler(mock_yhandler.YHandler())
    ids = gm.league_ids(year=2017)
    assert(len(ids) == 1)
    print(ids)
    assert(ids[0] == '370.l.56877')


def test_to_league(sc):
    gm = yfa.Game(sc, 'mlb')
    gm.inject_yhandler(mock_yhandler.YHandler())
    lg = gm.to_league('370.l.56877')
    assert(isinstance(lg, yfa.League))


def test_game_id(sc):
    gm = yfa.Game(sc, 'nhl')
    gm.inject_yhandler(mock_yhandler.YHandler())
    assert(gm.game_id() == '396')
