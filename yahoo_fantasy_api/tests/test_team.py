#!/bin/python

import json
from yahoo_fantasy_api import team
import os

# For testing, we don't call out to Yahoo!  We just use a sample json file.
# For that reason the OAuth2 session context can be None.
TEST_SESSION_CONTEXT = None


def matchup_gen(sc, team_key, week):
    dir_path = os.path.dirname(os.path.realpath(__file__))
    with open(dir_path + "/sample.matchup.json", "r") as f:
        return json.load(f)


def test_matchup():
    tm = team.Team(TEST_SESSION_CONTEXT, '268.l.46645')
    opponent = tm.matchup(3, data_gen=matchup_gen)
    assert(opponent == '388.l.27081.t.5')


def roster_gen(sc, team_key, week):
    dir_path = os.path.dirname(os.path.realpath(__file__))
    with open(dir_path + "/sample.team_roster.json", "r") as f:
        return json.load(f)


def test_roster():
    tm = team.Team(TEST_SESSION_CONTEXT, '268.l.46645')
    r = tm.roster(3, data_gen=roster_gen)
    print(r)
    assert(len(r) == 21)
    assert(r[20]['name'] == 'Brandon Woodruff')
    assert(r[20]['position_type'] == 'P')
    assert(r[20]['player_id'] == 10730)
    assert(r[20]['selected_position'] == 'BN')
    assert(r[5]['name'] == 'Juan Soto')
    assert(r[5]['position_type'] == 'B')
    assert(len(r[5]['eligible_positions']) == 2)
    assert(r[5]['eligible_positions'][0] == 'LF')
    assert(r[5]['eligible_positions'][1] == 'Util')
    assert(r[5]['selected_position'] == 'LF')
