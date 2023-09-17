#!/bin/python

import os


def test_matchup(mock_team):
    opponent = mock_team.matchup(3)
    assert(opponent == '388.l.27081.t.5')


def test_roster(mock_team):
    r = mock_team.roster(3)
    print(r)
    assert(len(r) == 22)
    print(r[21])
    assert(r[21]['name'] == 'Jack Flaherty')
    assert(r[21]['position_type'] == 'P')
    assert(r[21]['player_id'] == 10592)
    assert(r[21]['selected_position'] == 'IL')
    print(r[5])
    assert(r[5]['name'] == 'Yordan Alvarez')
    assert(r[5]['position_type'] == 'B')
    assert(len(r[5]['eligible_positions']) == 2)
    assert(r[5]['eligible_positions'][0] == 'LF')
    assert(r[5]['eligible_positions'][1] == 'Util')
    assert(r[5]['selected_position'] == 'LF')


def test_roster_status(mock_team):
    r = mock_team.roster(3)
    print(r)
    assert(r[0]['name'] == 'Danny Jansen')
    assert(r[0]['status'] == '')
    assert(r[0]['eligible_positions'] == ['C', 'Util'])
    assert(r[21]['name'] == 'Jack Flaherty')
    assert(r[21]['status'] == 'IL60')
    assert(r[21]['eligible_positions'] == ['SP', 'IL'])


def test_proposed_trades(mock_team):
    trs = mock_team.proposed_trades()
    print(trs)
    assert(len(trs) == 3)
    assert(trs[0]['transaction_key'] == '396.l.49770.pt.1')
    assert(len(trs[0]['trader_players']) == 1)
    assert(trs[0]['trader_players'][0]['name'] == 'Drew Doughty')
    assert(len(trs[0]['tradee_players']) == 1)
    assert(trs[0]['tradee_players'][0]['name'] == 'Jacob Trouba')
    assert(trs[1]['transaction_key'] == '396.l.49770.pt.2')
    assert(len(trs[1]['trader_players']) == 2)
    assert(trs[1]['trader_players'][0]['name'] == 'Claude Giroux')
    assert(trs[1]['trader_players'][1]['name'] == 'Tuukka Rask')
    assert(len(trs[1]['tradee_players']) == 2)
    assert(trs[1]['tradee_players'][0]['name'] == 'Aleksander Barkov')
    assert(trs[1]['tradee_players'][1]['name'] == 'Brayden Schenn')


def test__construct_trade_xml(mock_team):
    dir_path = os.path.dirname(os.path.realpath(__file__))
    with open(f'{dir_path}/accept_trade.xml', 'r') as file:
        expected_xml = file.read().replace('  ', '\t')

    transaction_key = '396.l.49770.pt.1'
    xml = mock_team._construct_trade_xml(transaction_key, action='accept',
                                         trade_note='Dude, that is a totally fair trade.')
    assert xml == expected_xml


def test__construct_trade_proposal_xml(mock_team):
    dir_path = os.path.dirname(os.path.realpath(__file__))
    with open(f'{dir_path}/trade_proposal.xml', 'r') as file:
        expected_xml = file.read().replace('  ', '\t')

    tradee_team_key = '248.l.55438.t.4'
    trade_note = 'Check out this trade proposal.'
    your_player_keys = ['248.p.4130']
    their_player_keys = ['248.p.2415']

    actual_xml = mock_team._construct_trade_proposal_xml(tradee_team_key, your_player_keys, their_player_keys, trade_note)

    assert actual_xml == expected_xml
