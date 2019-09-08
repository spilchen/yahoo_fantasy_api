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

    def get_players_raw(self, league_id, start, status, position=None):
        """Return the raw JSON when requesting players in the league

        The result is limited to 25 players.  the first 1000 players.

        :param league_id: League ID to get the players for
        :type league_id: str
        :param start: The output is paged at 25 players each time.  Use this
        parameter for subsequent calls to get the players at the next page.
        For example, you specify 0 for the first call, 25 for the second call,
        etc.
        :type start: int
        :param status: A filter to limit the player status.  Available values
        are: 'A' - all available; 'FA' - free agents; 'W' - waivers, 'T' -
        taken players, 'K' - keepers
        :type status: str
        :param position: A filter to return players only for a specific
        position.  If None is passed, then no position filtering occurs.
        :type position: str
        :return: JSON document of the request.
        """
        if position is None:
            pos_parm = ""
        else:
            pos_parm = ";position={}".format(position)
        return self.get("league/{}/players;start={};count=25;status={}{}".
                        format(league_id, start, status, pos_parm))
    
    def get_player_raw(self, league_id, player_name):
        """Return the raw JSON when requesting player details

        
        :param league_id: League ID to get the player for
        :type league_id: str
        :param player_name: Name of player to get the details for
        :type player_name: str
        :return: JSON document of the request.
        """
        player_stat_uri = ""
        if player_name is not None:
            player_stat_uri = "players;search={}/stats".format(player_name)
        return self.get("league/{}/{}".format(league_id, player_stat_uri))
