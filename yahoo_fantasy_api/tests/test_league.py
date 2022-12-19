#!/bin/python

from yahoo_fantasy_api.tests.conftest import mock_mlb_league
import yahoo_fantasy_api as yfa
import datetime
import pytest


def test_standings(mock_mlb_league):
    s = mock_mlb_league.standings()
    assert(len(s) == 10)
    assert(s[0]['name'] == "Lumber Kings")
    assert(s[0]['outcome_totals']['wins'] == '144')


def test_settings(mock_mlb_league):
    s = mock_mlb_league.settings()
    print(s)
    assert(s['name'] == "Buck you're next!")
    assert(s['scoring_type'] == "head")
    assert(int(s['start_week']) == 1)
    assert(int(s['end_week']) == 24)
    assert(s['start_date'] == '2019-03-20')
    assert(s['end_date'] == '2019-09-22')
    assert(s['game_code'] == 'mlb')
    assert(s['season'] == '2019')


def test_stat_categories(mock_mlb_league):
    s = mock_mlb_league.stat_categories()
    print(s)
    assert(len(s) == 12)
    assert(s[0]['display_name'] == 'R')
    assert(s[0]['position_type'] == 'B')
    assert(s[11]['display_name'] == 'NSV')
    assert(s[11]['position_type'] == 'P')


def test_to_team(mock_mlb_league):
    tm = mock_mlb_league.to_team('370.l.56877.t.5')
    assert(isinstance(tm, yfa.Team))


def test_team_key(mock_mlb_league):
    k = mock_mlb_league.team_key()
    print(k)
    assert(k == '370.l.56877.t.5')


def test_current_week(mock_mlb_league):
    wk = mock_mlb_league.current_week()
    print(wk)
    assert(wk == 12)


def test_end_week(mock_mlb_league):
    wk = mock_mlb_league.end_week()
    print(wk)
    assert(wk == 24)


def test_week_date_range(mock_mlb_league):
    (sdt, edt) = mock_mlb_league.week_date_range(12)
    print(sdt)
    assert(sdt == datetime.date(2019, 6, 17))
    print(edt)
    assert(edt == datetime.date(2019, 6, 23))


def test_week_date_range_past_current(mock_mlb_league):
    assert(mock_mlb_league.current_week() == 12)
    (sdt, edt) = mock_mlb_league.week_date_range(13)
    print(sdt)
    assert(sdt == datetime.date(2019, 6, 24))
    print(edt)
    assert(edt == datetime.date(2019, 6, 30))


def test_week_date_range_of_last(mock_mlb_league):
    with pytest.raises(RuntimeError):
        (sdt, edt) = mock_mlb_league.week_date_range(23)


def test_team_list(mock_mlb_league):
    tms = mock_mlb_league.teams()
    assert(len(tms) == 10)
    assert('370.l.56877.t.9' in tms)
    print(tms['370.l.56877.t.9'])
    assert(tms['370.l.56877.t.9']['name'] == 'Bobble Addicts')
    assert(tms['370.l.56877.t.9']['number_of_moves'] == '30')


def test_free_agents(mock_mlb_league):
    fa = mock_mlb_league.free_agents('C')
    print(fa)
    assert(len(fa) == 42)
    assert(fa[9]['name'] == 'Brad Richardson')
    assert(fa[9]['position_type'] == 'P')
    assert(fa[9]['player_id'] == 3704)
    assert(len(fa[9]['eligible_positions']) == 1)
    assert(fa[9]['eligible_positions'] == ['C'])
    assert(fa[15]['name'] == 'David Krejci')
    assert(fa[15]['status'] == 'DTD')
    assert(fa[21]['name'] == 'Derick Brassard')
    assert(fa[21]['position_type'] == 'P')
    assert(fa[21]['player_id'] == 3987)
    assert(len(fa[21]['eligible_positions']) == 2)
    assert(fa[21]['eligible_positions'] == ['C', 'LW'])


def test_pct_own_in_free_agents(mock_mlb_league):
    fa = mock_mlb_league.free_agents('C')
    print(fa)
    assert(len(fa) == 42)
    assert(fa[0]['name'] == 'Joe Thornton')
    assert(fa[0]['percent_owned'] == 7)
    assert(fa[8]['name'] == 'Nate Thompson')
    assert(fa[8]['percent_owned'] == 0)
    assert(fa[41]['name'] == 'Ryan O\'Reilly')
    assert(fa[41]['percent_owned'] == 92)


def test_percent_owned(mock_mlb_league):
    po = mock_mlb_league.percent_owned([3737, 6381, 4003, 3705])
    assert(len(po) == 4)
    assert(po[0]['player_id'] == 3737)
    assert(po[0]['name'] == 'Sidney Crosby')
    assert(po[0]['percent_owned'] == 100)
    assert(po[1]['player_id'] == 6381)
    assert(po[1]['name'] == 'Dylan Larkin')
    assert(po[1]['percent_owned'] == 89)


def test_ownership(mock_mlb_league):
    details = mock_mlb_league.ownership([9265, 27564])
    assert(details['9265']['owner_team_name'] == "Ladies and Edelman")
    assert(details['27564']['ownership_type'] == "freeagents")


def test_edit_date(mock_mlb_league):
    dt = mock_mlb_league.edit_date()
    assert(isinstance(dt, datetime.date))
    assert(dt == datetime.date(2019, 4, 1))


def test_positions(mock_mlb_league):
    ps = mock_mlb_league.positions()
    assert('DL' in ps)
    assert(ps['DL']['count'] == 3)
    assert('BN' in ps)
    assert(ps['BN']['count'] == 2)
    assert('2B' in ps)
    assert(ps['2B']['count'] == 1)
    assert(ps['2B']['position_type'] == 'B')


def test_mlb_player_stats(mock_mlb_league):
    stats = mock_mlb_league.player_stats([7345], 'season')
    assert(len(stats) == 24)
    assert(stats[0]['name'] == 'Yadier Molina')
    assert(isinstance(stats[0]['player_id'], int))
    assert(stats[0]['player_id'] == 7345)
    assert(stats[0]['HR'] == 10)


def test_nhl_player_stats(mock_nhl_league):
    stats = mock_nhl_league.player_stats([4002], 'season')
    print(stats)
    assert(len(stats) == 1)
    assert(stats[0]['name'] == 'Claude Giroux')
    assert(stats[0]['SOG'] == 147)
    assert(stats[0]['PTS'] == 35)


def test_draft_results(mock_nhl_league):
    dres = mock_nhl_league.draft_results()
    print(dres)
    assert(len(dres) == 84)
    assert(dres[83]['round'] == 14)
    assert(dres[83]['team_key'] == '396.l.49770.t.6')
    assert("player_key" not in dres[83])
    assert("player_id" in dres[83])
    assert(dres[83]['player_id'] == 5085)


def test_phil_player_details(mock_nhl_league):
    r = mock_nhl_league.player_details("Phil")
    print(r)
    assert(len(r) == 14)
    print(r[0])
    assert(r[0]['name']['full'] == 'Phil Kessel')
    print(r[8])
    assert(r[8]['name']['full'] == 'Matthew Phillips')


def test_blah_player_details(mock_nhl_league):
    r = mock_nhl_league.player_details("blah")
    print(r)
    assert(len(r) == 0)


def test_ids_player_details(mock_nhl_league):
    r = mock_nhl_league.player_details([3983, 5085, 5387])
    print(r)
    assert(len(r) == 3)
    assert(r[0]['name']['full'] == 'Phil Kessel')
    assert(r[1]['name']['full'] == 'Philipp Grubauer')
    assert(r[2]['name']['full'] == 'Phillip Danault')


def test_player_details_cache(mock_nhl_league):
    mock_nhl_league.player_details("Phil")
    mock_nhl_league.player_details([3983, 5085])
    mock_nhl_league.player_details(5387)
    exp_keys = ['Phil', 3983, 5085, 5387]
    assert(list(mock_nhl_league.player_details_cache.keys()) == exp_keys)


def test_transactions(mock_mlb_league):
    transactions = mock_mlb_league.transactions("trade", "1")
    for transaction in transactions:
        assert(transaction)
        assert(transaction['type'] == 'trade')
        assert(transaction['players'])


def test_get_team(mock_nhl_league):
    team = mock_nhl_league.get_team("LOS DIOSES")
    assert(team)
    assert(team["LOS DIOSES"].team_key == '418.l.15944.t.1')
