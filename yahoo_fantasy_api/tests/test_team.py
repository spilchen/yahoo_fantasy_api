#!/bin/python


def test_matchup(mock_team):
    opponent = mock_team.matchup(3)
    assert(opponent == '388.l.27081.t.5')


def test_roster(mock_team):
    r = mock_team.roster(3)
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


def test_roster_status(mock_team):
    r = mock_team.roster(3)
    print(r)
    assert(r[0]['name'] == 'Buster Posey')
    assert(r[0]['status'] == 'DTD')
    assert(r[0]['eligible_positions'] == ['C', '1B', 'Util'])
    assert(r[1]['name'] == 'Paul Goldschmidt')
    assert(r[1]['status'] == '')
    assert(r[1]['eligible_positions'] == ['1B', 'Util'])
