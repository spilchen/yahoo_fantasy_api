#!/bin/python

from yahoo_fantasy_api import yahoo_api
import objectpath


class Team:
    def __init__(self, sc, team_key):
        """Class initializer

        :param sc: Session context for oauth
        :type sc: OAuth2 from yahoo_oauth
        :param team_key: Team key identifier to find the matchups for
        :type team_key: str
        """
        self.sc = sc
        self.team_key = team_key

    def matchup(self, week, data_gen=yahoo_api.get_matchup_raw):
        """Return the team of the matchup my team is playing in a given week

        :param week: Week number to find the matchup for
        :type week: int
        :param data_gen: Optional data generation function.  Only used for
           testing purposes to avoid call-outs to Yahoo!  The function accepts
           3 parameters: sc (session context), team_key, week
        :type data_gen: function
        :return: Team key of the opponent

        >>> gm.matchup(3)
        388.l.27081.t.9
        """
        t = objectpath.Tree(data_gen(self.sc, self.team_key, week))
        json = t.execute('$..matchups..(team_key)')
        for k in json:
            if 'team_key' in k:
                this_team_key = k['team_key']
                if this_team_key != self.team_key:
                    return this_team_key
        raise RuntimeError("Could not find opponent")
