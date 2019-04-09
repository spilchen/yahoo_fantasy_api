#!/bin/python

from yahoo_fantasy_api import team
import mock_yhandler

# For testing, we don't call out to Yahoo!  We just use a sample json file.
# For that reason the OAuth2 session context can be None.
TEST_SESSION_CONTEXT = None


def test_matchup():
    tm = team.Team(TEST_SESSION_CONTEXT, '268.l.46645')
    tm.inject_yhandler(mock_yhandler.YHandler())
    opponent = tm.matchup(3)
    assert(opponent == '388.l.27081.t.5')


def test_roster():
    tm = team.Team(TEST_SESSION_CONTEXT, '268.l.46645')
    tm.inject_yhandler(mock_yhandler.YHandler())
    r = tm.roster(3)
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
