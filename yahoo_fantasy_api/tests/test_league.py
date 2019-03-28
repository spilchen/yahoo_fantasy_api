#!/bin/python

import json
from yahoo_fantasy_api import league
import os

# For testing, we don't call out to Yahoo!  We just use a sample json file.
# For that reason the OAuth2 session context can be None.
TEST_SESSION_CONTEXT = None


def league_teams_gen(sc):
    dir_path = os.path.dirname(os.path.realpath(__file__))
    with open(dir_path + "/sample.league_teams.json", "r") as f:
        return json.load(f)


def test_ids():
    lg = league.League(TEST_SESSION_CONTEXT)
    ids = lg.ids(data_gen=league_teams_gen)
    assert(len(ids) == 12)
    print(ids)
    assert(ids[5] == '268.l.46645')


def test_ids_for_year():
    lg = league.League(TEST_SESSION_CONTEXT)
    ids = lg.ids('2017', data_gen=league_teams_gen)
    assert(len(ids) == 1)
    print(ids)
    assert(ids[0] == '370.l.56877')


def standing_teams_gen(sc, league_id):
    dir_path = os.path.dirname(os.path.realpath(__file__))
    with open(dir_path + "/sample.standings.json", "r") as f:
        return json.load(f)


def test_standings():
    lg = league.League(TEST_SESSION_CONTEXT)
    s = lg.standings("370.l.56877", data_gen=standing_teams_gen)
    assert(len(s) == 10)
    assert(s[0] == "Lumber Kings")


def settings_gen(sc, league_id):
    dir_path = os.path.dirname(os.path.realpath(__file__))
    with open(dir_path + "/sample.league_settings.json", "r") as f:
        return json.load(f)


def test_settings():
    lg = league.League(TEST_SESSION_CONTEXT)
    s = lg.settings("370.l.56877", data_gen=settings_gen)
    print(s)
    assert(s['name'] == "Buck you're next!")
    assert(s['scoring_type'] == "head")
    assert(int(s['start_week']) == 1)
    assert(int(s['end_week']) == 24)
    assert(s['start_date'] == '2019-03-20')
    assert(s['end_date'] == '2019-09-22')
    assert(s['game_code'] == 'mlb')
    assert(s['season'] == '2019')
