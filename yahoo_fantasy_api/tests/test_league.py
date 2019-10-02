#!/bin/python

import yahoo_fantasy_api as yfa
import datetime
import pytest


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
    assert(type(tm) is yfa.Team)


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


def test_week_date_range_past_current(mock_league):
    assert(mock_league.current_week() == 12)
    (sdt, edt) = mock_league.week_date_range(13)
    print(sdt)
    assert(sdt == datetime.date(2019, 6, 24))
    print(edt)
    assert(edt == datetime.date(2019, 6, 30))


def test_week_date_range_of_last(mock_league):
    with pytest.raises(RuntimeError):
        (sdt, edt) = mock_league.week_date_range(23)


def test_team_list(mock_league):
    tms = mock_league.teams()
    print(tms)
    assert(len(tms) == 10)
    assert(tms[8]['name'] == 'Bobble Addicts')
    assert(tms[8]['team_key'] == '370.l.56877.t.9')


def test_free_agents(mock_league):
    fa = mock_league.free_agents('C')
    print(fa)
    assert(len(fa) == 36)
    assert(fa[8]['name'] == 'Brad Richardson')
    assert(fa[8]['position_type'] == 'P')
    assert(fa[8]['player_id'] == 3704)
    assert(len(fa[8]['eligible_positions']) == 1)
    assert(fa[8]['eligible_positions'] == ['C'])
    assert(fa[12]['name'] == 'David Krejci')
    assert(fa[12]['status'] == 'DTD')
    assert(fa[17]['name'] == 'Derick Brassard')
    assert(fa[17]['position_type'] == 'P')
    assert(fa[17]['player_id'] == 3987)
    assert(len(fa[17]['eligible_positions']) == 2)
    assert(fa[17]['eligible_positions'] == ['C', 'LW'])


def test_pct_own_in_free_agents(mock_league):
    fa = mock_league.free_agents('C')
    print(fa)
    assert(len(fa) == 36)
    assert(fa[0]['name'] == 'Joe Thornton')
    assert(fa[0]['percent_owned'] == 7)
    assert(fa[7]['name'] == 'Nate Thompson')
    assert(fa[7]['percent_owned'] == 0)
    assert(fa[35]['name'] == 'Ryan O\'Reilly')
    assert(fa[35]['percent_owned'] == 92)


def test_percent_owned(mock_league):
    po = mock_league.percent_owned([3737, 6381, 4003, 3705])
    assert(len(po) == 4)
    assert(po[0]['player_id'] == 3737)
    assert(po[0]['name'] == 'Sidney Crosby')
    assert(po[0]['percent_owned'] == 100)
    assert(po[1]['player_id'] == 6381)
    assert(po[1]['name'] == 'Dylan Larkin')
    assert(po[1]['percent_owned'] == 89)
