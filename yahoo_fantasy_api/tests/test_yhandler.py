#!/bin/python

from yahoo_fantasy_api import yhandler
from unittest.mock import MagicMock
import datetime


def test_matchup(mock_team):
    opponent = mock_team.matchup(3)
    assert(opponent == '388.l.27081.t.5')


def test_roster_raw():
    yh = yhandler.YHandler('dummy-sc')
    yh.get = MagicMock(return_value=None)
    team_key = '1234'
    yh.get_roster_raw(team_key, week=10)
    yh.get.assert_called_with("team/{}/roster;week=10".format(team_key))
    yh.get_roster_raw(team_key, day=datetime.date(2019, 10, 7))
    yh.get.assert_called_with("team/{}/roster;date=2019-10-07".format(
        team_key))
    yh.get_roster_raw(team_key)
    yh.get.assert_called_with("team/{}/roster".format(team_key))


def test_game_raw():
    yh = yhandler.YHandler('dummy-sc')
    yh.get = MagicMock(return_value=None)
    game_code = "nfl"
    yh.get_game_raw(game_code)
    yh.get.assert_called_with("game/{}".format(game_code))


def test_player_ownership_raw():
    yh = yhandler.YHandler('dummy-sc')
    yh.get = MagicMock(return_value=None)
    league_id = "399.l.710921"
    player_ids = [9265]
    joined_ids = ",".join(["399.p." + str(i) for i in player_ids])
    yh.get_player_ownership_raw(league_id, player_ids)
    yh.get.assert_called_with("league/{}/players;player_keys={}/ownership".format(league_id, joined_ids))


def test_get_transactions_raw():
    yh = yhandler.YHandler('dummy-sc')
    yh.get = MagicMock(return_value=None)
    league_id = "399.l.710921"
    tran_types = "trade"
    count = ""
    expected = "league/{}/transactions;types={};count={}".format(league_id, tran_types, str(count))
    yh.get_transactions_raw(league_id, tran_types, count)
    yh.get.assert_called_with(expected)
    yh.get_transactions_raw(league_id, tran_types, "")
    expected = "league/{}/transactions;types={};count={}".format(league_id, tran_types, "")
    yh.get.assert_called_with(expected)


def test_league_teams_raw():
    yh = yhandler.YHandler('dummy-sc')
    yh.get = MagicMock(return_value=None)
    league_id = "399.l.710921"
    yh.get_league_teams_raw(league_id)
    yh.get.assert_called_with("league/{}/teams".format(league_id))
