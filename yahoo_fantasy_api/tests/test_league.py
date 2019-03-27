#!/bin/python

import json
from yahoo_fantasy_api import league
import os


def league_teams_gen(sc):
    dir_path = os.path.dirname(os.path.realpath(__file__))
    with open(dir_path + "/sample.league_teams.json", "r") as f:
        return json.load(f)


def test_ids():
    lg = league.League(None)
    ids = lg.ids(data_gen=league_teams_gen)
    assert(len(ids) == 12)
    print(ids)
    assert(ids[5] == '268.l.46645')


def test_ids_for_year():
    lg = league.League(None)
    ids = lg.ids('2017', data_gen=league_teams_gen)
    assert(len(ids) == 1)
    print(ids)
    assert(ids[0] == '370.l.56877')


def standing_teams_gen(sc, league_id):
    dir_path = os.path.dirname(os.path.realpath(__file__))
    with open(dir_path + "/sample.standings.json", "r") as f:
        return json.load(f)


def test_standings():
    lg = league.League(None)
    s = lg.standings("370.l.56877", data_gen=standing_teams_gen)
    assert(len(s) == 10)
    assert(s[0] == "Lumber Kings")
