#!/usr/bin/env python

"""Use the game and league API

Usage:
  league.py <json> <game_code> [<year>]

  <json>       The name of the JSON that has bearer token.  This can be
               generated from init_oauth_env.py.
  <game_code>  The game code of the league you want to lookup.  Use 'mlb' for a
               baseball league and 'nhl' for a hockey league.
  <year>       Optional year that will filter only leagues that match this year
"""
from docopt import docopt
from yahoo_oauth import OAuth2
from yahoo_fantasy_api import league, game


if __name__ == '__main__':
    args = docopt(__doc__, version='1.0')
    sc = OAuth2(None, None, from_file=args['<json>'])
    gm = game.Game(sc, args['<game_code>'])
    ids = gm.league_ids(year=args['<year>'])
    for lg_id in ids:
        if lg_id.find("auto") > 0:
            continue
        lg = league.League(sc, lg_id)
        standings = lg.standings()
        print("")
        print(lg_id)
        for i, t in zip(range(1, 100), standings):
            print("{} - {}".format(i, t))
        print("")
        print(lg.settings())
