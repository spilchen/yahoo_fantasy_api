#!/bin/python

from yahoo_fantasy_api import yahoo_api, league
import objectpath


class Game:
    def __init__(self, sc, code):
        """Class initializer

        :param sc: OAuth2 session context from yahoo_oauth
        :type sc: OAuth2
        :param code: Sport code (mlb, nhl, etc)
        :type code: str.
        """
        self.sc = sc
        self.code = code

    def to_league(self, league_id):
        """Construct a League object from a Game

        :param league_id: League ID of the new League to construct
        :type league_id: str
        :return: League object
        """
        return league.League(self.sc, league_id)

    def league_ids(self, year=None, data_gen=yahoo_api.get_teams_raw):
        """Return the Yahoo! league IDs that the current user played in

        :param year: Optional year, used to filter league IDs returned.
        :type year: int
        :param data_gen: Optional data generation function.  This exists for
            test purposes to allow for test dependency injection.  The default
            value for this parameter is the Yahoo! API.
        :returns: List of league ids
        """
        t = objectpath.Tree(data_gen(self.sc))
        jfilter = t.execute('$..(team_key,season,code)')
        league_applies = False
        ids = []
        for row in jfilter:
            # We'll see two types of rows that come out of objectpath filter.
            # A row that has the season/code, then all of the leagues that it
            # applies too.  Check if the subsequent league applies each time we
            # get the season/code pair.
            if 'season' in row and 'code' in row:
                league_applies = row['code'] == self.code
                if league_applies is True and year is not None:
                    league_applies = int(row['season']) == int(year)
            elif league_applies:
                assert('team_key' in row)
                ids.append(self._extract_id_from_team_key(row['team_key']))
        # Return leagues in deterministic order
        ids.sort()
        return ids

    def _extract_id_from_team_key(self, t):
        """Given a team key, extract just the league id from it

        A team key is defined as:
            <game#>.l.<league#>.t.<team#>
        """
        assert(t.find(".t.") > 0), "Doesn't look like a valid team key: " + t
        return t[0:t.find(".t.")]
