#!/bin/python

from yahoo_fantasy_api import yhandler, league
import objectpath


class Game:
    """Abstraction for a Yahoo! fantasy game

    :param sc: Fully constructed session context
    :type sc: :class:`yahoo_oauth.OAuth2`
    :param code: Sport code (mlb, nhl, etc)
    :type code: str
    """

    def __init__(self, sc, code):
        self.sc = sc
        self.code = code
        self.yhandler = yhandler.YHandler(sc)

    def inject_yhandler(self, yhandler):
        self.yhandler = yhandler

    def game_id(self):
        """Return the Yahoo! Game ID
        :return: Game ID
        :rtype: str
        """
        t = objectpath.Tree(self.yhandler.get_game_raw(self.code))
        jfilter = t.execute('$..(game_id)')
        id = ''
        for row in jfilter:
            id = row['game_id']
        return id

    def to_league(self, league_id):
        """Construct a League object from a Game

        :param league_id: League ID of the new League to construct
        :type league_id: str
        :return: Fully constructed object
        :rtype: League
        """
        lg = league.League(self.sc, league_id, handler=self.yhandler)
        return lg

    def league_ids(self, year=None, is_available=False, game_types=None, game_codes=None, seasons=None):
        """Return the Yahoo! league IDs that the current user played in

        :param year: Optional year, when provide _league_ids_deprecated() will be used to fetch the league ids 
        :type is_available: int
        :param is_available: Optional flag to filter out leagues that are not available
        :type is_available: bool
        :param game_types: Optional list of game types to filter league IDs returned. Valid values are full|pickem-team|pickem-group|pickem-team-list
        :type game_types: list[str]
        :param game_codes: Optional list of game codes(i.e. nfl, mlb, nhl, nba) to filter league IDs returned.
        :type game_codes: list[str]
        :param seasons: Optional list of seasons to filter league IDs returned.
        :type seasons: list[str]
        :returns: List of league ids
        """
        if year is not None:
            return self._league_ids_deprecated(year=year)

        t = objectpath.Tree(self.yhandler.get_leagues_raw(is_available=is_available, game_types=game_types, game_codes=game_codes,seasons=seasons))
        ids = list(t.execute('$..league_key'))
        return ids

    def _league_ids_deprecated(self, year=None):
        """Return the Yahoo! league IDs that the current user played in

        :param year: Optional year, used to filter league IDs returned.
        :type year: int
        :returns: List of league ids
        """
        t = objectpath.Tree(self.yhandler.get_teams_raw())
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
