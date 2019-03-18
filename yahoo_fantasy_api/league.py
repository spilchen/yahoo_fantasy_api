#!/bin/python

from yahoo_fantasy_api import yahoo_api
import objectpath


def get_teams_raw(sc):
    """Return the raw JSON when requesting the logged in players teams.

    Args:
        sc OAuth2 session context.

    Returns:
        JSON document of the request.
    """
    return yahoo_api.get(sc, "users;use_login=1/games/teams")


def get_standings_raw(sc, league_id):
    """Return the raw JSON when requesting standings for a league.

    Args:
        sc OAuth2 session context.
        league_id League ID to get the standings for

    Returns:
        JSON document of the request.
    """
    return yahoo_api.get(sc, "league/{}/standings".format(league_id))


def get_settings_raw(sc, league_id):
    """Return the raw JSON when requesting settings for a league.

    Args:
        sc OAuth2 session context.
        league_id League ID to get the settings for

    Returns:
        JSON document of the request.
    """
    return yahoo_api.get(sc, "league/{}/settings".format(league_id))


class League:
    def __init__(self, sc, code):
        """Class initializer

        Args:
            sc OAuth2 session context
            code Sport code (mlb, nhl, etc)
        """
        self.sc = sc
        self.code = code

    def ids(self, year=None, data_gen=get_teams_raw):
        """Return the Yahoo! league IDs that the current user played in

        Args:
            year (optional) Will only return league IDs from the given year
            data_gen (optional) Data generation function.  This exists for test
                 purposes to allow for test dependency injection.  The default
                value for this parameter is the Yahoo! API.

        Return:
            List of league ids
        """
        json = data_gen(self.sc)
        t = objectpath.Tree(json)
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
                ids.append(_extract_id_from_team_key(row['team_key']))
        # Return leagues in deterministic order
        ids.sort()
        return ids

    def standings(self, league_id, data_gen=get_standings_raw):
        """Return the standings of the given league id

        Args:
            league_id League id to get the standings for

        Returns:
            An ordered list of the teams in the standings.  First entry is the
            first place team.
        """
        json = data_gen(self.sc, league_id)
        team_json = \
            json['fantasy_content']["league"][1]["standings"][0]["teams"]
        standings = []
        for i in range(team_json["count"]):
            team = team_json[str(i)]["team"][0]
            standings.append(team[2]['name'])
        return standings

    def settings(self, league_id, data_gen=get_settings_raw):
        json = data_gen(self.sc, league_id)
        t = objectpath.Tree(json)
        settings_to_return = """
        name, scoring_type,
        start_week, current_week, end_week,start_date, end_date,
        game_code, season
        """
        return t.execute('$.fantasy_content.league.({})[0]'.format(
            settings_to_return))


def _extract_id_from_team_key(t):
    """Given a team key, extract just the league id from it

    A team key is defined as:
        <game#>.l.<league#>.t.<team#>
    """
    assert(t.find(".t.") > 0), "Doesn't look like a valid team key: " + t
    return t[0:t.find(".t.")]
