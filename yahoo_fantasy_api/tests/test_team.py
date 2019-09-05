#!/bin/python

import yahoo_fantasy_api as yfa
import mock_yhandler


def test_matchup(sc):
    tm = yfa.Team(sc, '268.l.46645')
    tm.inject_yhandler(mock_yhandler.YHandler())
    opponent = tm.matchup(3)
    assert(opponent == '388.l.27081.t.5')


def test_roster(sc):
    tm = yfa.Team(sc, '268.l.46645')
    tm.inject_yhandler(mock_yhandler.YHandler())
    r = tm.roster(3)
    print(r)
    assert(len(r) == 25)
    print(r[21])
    assert(r[21]['name'] == 'Brandon Woodruff')
    assert(r[21]['position_type'] == 'P')
    assert(r[21]['player_id'] == 10730)
    assert(r[21]['selected_position'] == 'BN')
    print(r[5])
    assert(r[5]['name'] == 'Juan Soto')
    assert(r[5]['position_type'] == 'B')
    assert(len(r[5]['eligible_positions']) == 2)
    assert(r[5]['eligible_positions'][0] == 'LF')
    assert(r[5]['eligible_positions'][1] == 'Util')
    assert(r[5]['selected_position'] == 'LF')
