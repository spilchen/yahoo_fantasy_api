#!/bin/python

"""Use the team API

Usage:
  team.py <json>

  <json>  The name of the JSON that has bearer token.  This can be generated
          from init_oauth_env.py.
"""
from docopt import docopt
from yahoo_oauth import OAuth2
from yahoo_fantasy_api import league, game, team


if __name__ == '__main__':
    args = docopt(__doc__, version='1.0')
    print(args)
    sc = OAuth2(None, None, from_file=args['<json>'])
    gm = game.Game(sc, 'mlb')
    league_id = gm.league_ids(year=2019)
    lg = league.League(sc, league_id[0])
    team_key = lg.team_key()
    tm = team.Team(sc, team_key)
    print(tm.matchup(3))
    print(tm.roster(4))
