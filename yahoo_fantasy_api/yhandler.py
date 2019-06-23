#!/bin/python

import json

YAHOO_ENDPOINT = 'https://fantasysports.yahooapis.com/fantasy/v2'


class YHandler:
    """Class that constructs the APIs to send to Yahoo"""

    def __init__(self, sc):
        self.sc = sc

    def get(self, uri):
        """Send an API request to the URI and return the response as JSON

        :param uri: URI of the API to call
        :type uri: str
        :return: JSON document of the reponse
        :raises: RuntimeError if any response comes back with an error
        """
        response = self.sc.session.get("{}/{}".format(YAHOO_ENDPOINT, uri),
                                       params={'format': 'json'})
        jresp = response.json()
        if "error" in jresp:
            raise RuntimeError(json.dumps(jresp))
        return jresp

    def get_teams_raw(self):
        """Return the raw JSON when requesting the logged in players teams.

        :return: JSON document of the request.
        """
        return self.get("users;use_login=1/games/teams")

    def get_standings_raw(self, league_id):
        """Return the raw JSON when requesting standings for a league.

        :param league_id: League ID to get the standings for
        :type league_id: str
        :return: JSON document of the request.
        """
        return self.get("league/{}/standings".format(league_id))

    def get_settings_raw(self, league_id):
        """Return the raw JSON when requesting settings for a league.

        :param league_id: League ID to get the standings for
        :type league_id: str
        :return: JSON document of the request.
        """
        return self.get("league/{}/settings".format(league_id))

    def get_matchup_raw(self, team_key, week):
        """Return the raw JSON when requesting match-ups for a team

        :param team_key: Team key identifier to find the matchups for
        :type team_key: str
        :param week: What week number to request the matchup for?
        :type week: int
        :return: JSON of the request
        """
        return self.get("team/{}/matchups;weeks={}".format(team_key, week))

    def get_roster_raw(self, team_key, week):
        """Return the raw JSON when requesting a team's roster

        :param team_key: Team key identifier to find the matchups for
        :type team_key: str
        :param week: What week number to request the matchup for?
        :type week: int
        :return: JSON of the request
        """
        return self.get("team/{}/roster;week={}".format(team_key, week))

    def get_scoreboard_raw(self, league_id, week=None):
        """Return the raw JSON when requesting the scoreboard for a week

        :param league_id: League ID to get the standings for
        :type league_id: str
        :param week: The week number to request the scoreboard for
        :type week: int
        :return: JSON document of the request.
        """
        week_uri = ""
        if week is not None:
            week_uri = ";week={}".format(week)
        return self.get("league/{}/scoreboard{}".format(league_id, week_uri))
