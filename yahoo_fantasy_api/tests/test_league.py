#!/bin/python

from yahoo_fantasy_api import league, team
import mock_yhandler


def test_standings(sc):
    lg = league.League(sc, '370.l.36877')
    lg.inject_yhandler(mock_yhandler.YHandler())
    s = lg.standings()
    assert(len(s) == 10)
    assert(s[0] == "Lumber Kings")


def test_settings(sc):
    lg = league.League(sc, '370.l.56877')
    lg.inject_yhandler(mock_yhandler.YHandler())
    s = lg.settings()
    print(s)
    assert(s['name'] == "Buck you're next!")
    assert(s['scoring_type'] == "head")
    assert(int(s['start_week']) == 1)
    assert(int(s['end_week']) == 24)
    assert(s['start_date'] == '2019-03-20')
    assert(s['end_date'] == '2019-09-22')
    assert(s['game_code'] == 'mlb')
    assert(s['season'] == '2019')


def test_stat_categories(sc):
    lg = league.League(sc, '370.l.56877')
    lg.inject_yhandler(mock_yhandler.YHandler())
    s = lg.stat_categories()
    print(s)
    assert(len(s) == 12)
    assert(s[0]['display_name'] == 'R')
    assert(s[0]['position_type'] == 'B')
    assert(s[11]['display_name'] == 'NSV')
    assert(s[11]['position_type'] == 'P')


def test_to_team(sc):
    lg = league.League(sc, '370.l.56877')
    lg.inject_yhandler(mock_yhandler.YHandler())
    tm = lg.to_team('370.l.56877.t.5')
    assert(type(tm) is team.Team)


def test_team_key(sc):
    lg = league.League(sc, '370.l.56877')
    lg.inject_yhandler(mock_yhandler.YHandler())
    k = lg.team_key()
    print(k)
    assert(k == '370.l.56877.t.5')
