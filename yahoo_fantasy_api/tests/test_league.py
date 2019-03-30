#!/bin/python

import json
from yahoo_fantasy_api import league
import os

# For testing, we don't call out to Yahoo!  We just use a sample json file.
# For that reason the OAuth2 session context can be None.
TEST_SESSION_CONTEXT = None


def standing_teams_gen(sc, league_id):
    dir_path = os.path.dirname(os.path.realpath(__file__))
    with open(dir_path + "/sample.standings.json", "r") as f:
        return json.load(f)


def test_standings():
    lg = league.League(TEST_SESSION_CONTEXT, '370.l.36877')
    s = lg.standings(data_gen=standing_teams_gen)
    assert(len(s) == 10)
    assert(s[0] == "Lumber Kings")


def settings_gen(sc, league_id):
    dir_path = os.path.dirname(os.path.realpath(__file__))
    with open(dir_path + "/sample.league_settings.json", "r") as f:
        return json.load(f)


def test_settings():
    lg = league.League(TEST_SESSION_CONTEXT, '370.l.56877')
    s = lg.settings(data_gen=settings_gen)
    print(s)
    assert(s['name'] == "Buck you're next!")
    assert(s['scoring_type'] == "head")
    assert(int(s['start_week']) == 1)
    assert(int(s['end_week']) == 24)
    assert(s['start_date'] == '2019-03-20')
    assert(s['end_date'] == '2019-09-22')
    assert(s['game_code'] == 'mlb')
    assert(s['season'] == '2019')


def test_stat_categories():
    lg = league.League(TEST_SESSION_CONTEXT, '370.l.56877')
    s = lg.stat_categories(data_gen=settings_gen)
    print(s)
    assert(len(s) == 12)
    assert(s[0]['display_name'] == 'R')
    assert(s[0]['position_type'] == 'B')
    assert(s[11]['display_name'] == 'NSV')
    assert(s[11]['position_type'] == 'P')
