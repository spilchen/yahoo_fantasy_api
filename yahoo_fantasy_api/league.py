#!/bin/python

from yahoo_fantasy_api import yahoo_api


def get_teams_raw(sc):
    """Return the raw JSON when requesting the logged in players teams.

    Args:
        sc OAuth2 session context.

    Returns:
        JSON document of the request.
    """
    return yahoo_api.get(sc, "users;use_login=1/games/teams")


def get_standings_raw(sc, league_id):
    """Return the raw JSON when requesting the logged in players teams.

    Args:
        sc OAuth2 session context.
        league_id League ID to get the standings for

    Returns:
        JSON document of the request.
    """
    return yahoo_api.get(sc, "league/{}/standings".format(league_id))


class League:
    def __init__(self, sc):
        """Class initializer

        Args:
            sc OAuth2 session context
        """
        self.sc = sc

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
        return _get_ids_for_users(json["fantasy_content"]["users"], year)

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


def _get_ids_for_users(json, year):
    ids = []
    num = json["count"]
    for i in range(num):
        ids = ids + _get_ids_for_user(json[str(i)], year)
    return ids


def _get_ids_for_user(json, year):
    ids = []
    jgames = json["user"][1]["games"]
    num_games = jgames["count"]
    for i in range(num_games):
        league_id = _get_ids_for_game(jgames[str(i)], year)
        if league_id is not None:
            ids = ids + league_id
    return ids


def _get_ids_for_game(json, year):
    jgame = json["game"][0]
    if jgame["code"] == "mlb" and \
            (year is None or jgame["season"] == str(year)):
        jteams = json["game"][1]["teams"]
        ids = []
        count = jteams["count"]
        for i in range(count):
            ids.append(_get_ids_for_team_in_game(jteams[str(i)]))
        return ids
    else:
        return None


def _get_ids_for_team_in_game(json):
    jteam = json["team"]
    if "team_key" in jteam:
        return _extract_id_from_team_key(jteam["team_key"])
    else:
        for e in jteam[0]:
            if "team_key" in e:
                return _extract_id_from_team_key(e["team_key"])
        assert(False), jteam


def _extract_id_from_team_key(t):
    """Given a team key, extract just the league id from it

    A team key is defined as:
        <game#>.l.<league#>.t.<team#>
    """
    assert(t.find(".t.") > 0), "Doesn't look like a valid team key: " + t
    return t[0:t.find(".t.")]
