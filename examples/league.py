#!/bin/python

"""Use the league API

Usage:
  init_oauth_env.py <json>

  <json>  The name of the JSON that has bearer token
"""
from docopt import docopt
from yahoo_oauth import OAuth2
from yahoo_fantasy_api import league


if __name__ == '__main__':
    args = docopt(__doc__, version='1.0')
    print(args)
    sc = OAuth2(None, None, from_file=args['<json>'])
    lg = league.League(sc)
    ids = lg.ids()
    print(ids)
    league_id = lg.ids(year=2019)
    print(league_id)
    for lg_id in ids:
        if lg_id.find("auto") > 0:
            continue
        standings = lg.standings(lg_id)
        for i, t in zip(range(1, 100), standings):
            print("{} - {}".format(i, t))

    settings = lg.settings(league_id[0])
    print(settings)
