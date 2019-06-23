#!/bin/python

from yahoo_fantasy_api import team
import datetime


def test_standings(mock_league):
    s = mock_league.standings()
    assert(len(s) == 10)
    assert(s[0] == "Lumber Kings")


def test_settings(mock_league):
    s = mock_league.settings()
    print(s)
    assert(s['name'] == "Buck you're next!")
    assert(s['scoring_type'] == "head")
    assert(int(s['start_week']) == 1)
    assert(int(s['end_week']) == 24)
    assert(s['start_date'] == '2019-03-20')
    assert(s['end_date'] == '2019-09-22')
    assert(s['game_code'] == 'mlb')
    assert(s['season'] == '2019')


def test_stat_categories(mock_league):
    s = mock_league.stat_categories()
    print(s)
    assert(len(s) == 12)
    assert(s[0]['display_name'] == 'R')
    assert(s[0]['position_type'] == 'B')
    assert(s[11]['display_name'] == 'NSV')
    assert(s[11]['position_type'] == 'P')


def test_to_team(mock_league):
    tm = mock_league.to_team('370.l.56877.t.5')
    assert(type(tm) is team.Team)


def test_team_key(mock_league):
    k = mock_league.team_key()
    print(k)
    assert(k == '370.l.56877.t.5')


def test_current_week(mock_league):
    wk = mock_league.current_week()
    print(wk)
    assert(wk == 12)


def test_end_week(mock_league):
    wk = mock_league.end_week()
    print(wk)
    assert(wk == 24)

def test_week_date_range(mock_league):
    (sdt, edt) = mock_league.week_date_range(12)
    print(sdt)
    assert(sdt == datetime.date(2019, 6, 17))
    print(edt)
    assert(edt == datetime.date(2019, 6, 23))
