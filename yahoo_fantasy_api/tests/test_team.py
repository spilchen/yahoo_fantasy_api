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
