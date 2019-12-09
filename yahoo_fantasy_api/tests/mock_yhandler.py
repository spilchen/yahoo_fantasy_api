#!/bin/python

import json
import os


class YHandler:
    """A mocking class to return pre-canned JSON response for the various APIs

    This is used for testing purposes as we can avoid calling out to the Yahoo!
    service.
    """
    def __init__(self):
        self.dir_path = os.path.dirname(os.path.realpath(__file__))

    def get_teams_raw(self):
        """Return the raw JSON when requesting the logged in players teams.

        :return: JSON document of the request.
        """
        with open(self.dir_path + "/sample.league_teams.json", "r") as f:
            return json.load(f)

    def get_standings_raw(self, league_id):
        """Return the raw JSON when requesting standings for a league.

        :param league_id: League ID to get the standings for
        :type league_id: str
        :return: JSON document of the request.
        """
        with open(self.dir_path + "/sample.standings.json", "r") as f:
            return json.load(f)

    def get_settings_raw(self, league_id):
        """Return the raw JSON when requesting settings for a league.

        :param league_id: League ID to get the standings for
        :type league_id: str
        :return: JSON document of the request.
        """
        with open(self.dir_path + "/sample.league_settings.json", "r") as f:
            return json.load(f)

    def get_matchup_raw(self, team_key, week):
        """Return the raw JSON when requesting match-ups for a team

        :param team_key: Team key identifier to find the matchups for
        :type team_key: str
        :param week: What week number to request the matchup for?
        :type week: int
        :return: JSON of the request
        """
        with open(self.dir_path + "/sample.matchup.json", "r") as f:
            return json.load(f)

    def get_roster_raw(self, team_key, week=None, day=None):
        """Return the raw JSON when requesting a team's roster

        :param team_key: Team key identifier to find the matchups for
        :type team_key: str
        :param week: What week number to request the roster for?
        :type week: int
        :param day: What day number to request the roster
        :type day: datetime.date
        :return: JSON of the request
        """
        with open(self.dir_path + "/sample.team_roster.json", "r") as f:
            return json.load(f)

    def get_scoreboard_raw(self, league_id, week=None):
        """Return the raw JSON when requesting the scoreboard for a week

        :param league_id: League ID to get the standings for
        :type league_id: str
        :param week: The week number to request the scoreboard for
        :type week: int
        :return: JSON document of the request.
        """
        if week is None:
            fn = self.dir_path + "/sample.scoreboard.noweek.json"
        else:
            fn = self.dir_path + "/sample.scoreboard.week12.json"
        with open(fn, "r") as f:
            return json.load(f)

    def get_players_raw(self, league_id, start, status, position=None):
        assert(position == "C"), "Position must be 2B for mock"
        assert(status == "FA"), "FreeAgents only for mock"
        if start == 0:
            pg = "1"
        elif start == 25:
            pg = "2"
        else:
            assert(start == 50)
            pg = "3"
        fn = self.dir_path + "/sample.players.freeagents.C.pg.{}.json"\
            .format(pg)
        with open(fn, "r") as f:
            return json.load(f)

    def get_percent_owned_raw(self, league_id, player_ids):
        fn = self.dir_path + "/sample.percent_owned.json"
        with open(fn, "r") as f:
            return json.load(f)

    def get_team_transactions(self, league_id, team_key, tran_type):
        fn = self.dir_path + "/sample.pending_trade_transaction.json"
        with open(fn, "r") as f:
            return json.load(f)

    def get_player_stats_raw(self, game_code, player_ids, req_type, day,
                             season):
        fn = self.dir_path + "/sample.player_stats.json"
        with open(fn, "r") as f:
            return json.load(f)
