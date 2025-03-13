#!/bin/python

import yahoo_fantasy_api as yfa
import mock_yhandler


def test_ids(sc):
    gm = yfa.Game(sc, 'mlb')
    gm.inject_yhandler(mock_yhandler.YHandler())
    ids = gm.league_ids()
    for i in ids:
        print(i)
    assert(len(ids) == 2)
    print(ids)
    assert(ids[1] == '458.l.48797')


def test_ids_for_year(sc):
    gm = yfa.Game(sc, 'mlb')
    gm.inject_yhandler(mock_yhandler.YHandler())
    ids = gm.league_ids(seasons=[2017])
    print(ids)
    assert(ids[0] == '449.l.751781')


def test_to_league(sc):
    gm = yfa.Game(sc, 'mlb')
    gm.inject_yhandler(mock_yhandler.YHandler())
    lg = gm.to_league('370.l.56877')
    assert(isinstance(lg, yfa.League))


def test_game_id(sc):
    gm = yfa.Game(sc, 'nhl')
    gm.inject_yhandler(mock_yhandler.YHandler())
    assert(gm.game_id() == '396')
