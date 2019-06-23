#!/bin/python

"""Use the game and league API

Usage:
  league.py <json>

  <json>  The name of the JSON that has bearer token.  This can be generated
          from init_oauth_env.py.
"""
from docopt import docopt
from yahoo_oauth import OAuth2
from yahoo_fantasy_api import league, game


if __name__ == '__main__':
    args = docopt(__doc__, version='1.0')
    print(args)
    sc = OAuth2(None, None, from_file=args['<json>'])
    gm = game.Game(sc, 'mlb')
    ids = gm.league_ids()
    print(ids)
    for lg_id in ids:
        if lg_id.find("auto") > 0:
            continue
        lg = league.League(sc, lg_id)
        standings = lg.standings()
        for i, t in zip(range(1, 100), standings):
            print("{} - {}".format(i, t))

    league_id = gm.league_ids(year=2019)
    print(league_id)
    lg = gm.to_league(league_id[0])
    settings = lg.settings()
    print(settings)
    print(lg.team_key())
    print("Current Week = {}".format(lg.current_week()))
