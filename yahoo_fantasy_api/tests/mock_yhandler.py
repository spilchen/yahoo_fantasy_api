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
        with open(self.dir_path + "/sample.users_teams.json", "r") as f:
            return json.load(f)

    def get_league_teams_raw(self, league_id):
        """Return the raw JSON when requesting the teams for the current league.

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
        if league_id == '396.l.21484':
            id = '396.l.21484'
        else:
            id = "388.l.27081"
        fn = "{}/sample.league_settings.{}.json".format(self.dir_path, id)
        with open(fn, "r") as f:
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

    def get_player_ownership_raw(self, league_id, player_ids):
        if player_ids == 27564:
            fn = self.dir_path + "/sample.player_ownership_freeagent.json"
            with open(fn, "r") as f:
                return json.load(f)
        else:
            fn = self.dir_path + "/sample.player_ownership.json"
            with open(fn, "r") as f:
                return json.load(f)

    def get_team_transactions(self, league_id, team_key, tran_type):
        fn = self.dir_path + "/sample.pending_trade_transaction.json"
        with open(fn, "r") as f:
            return json.load(f)

    def get_player_stats_raw(self, game_code, player_ids, req_type, day,
                             week, season):
        if game_code == 'nhl':
            id = "396.l.21484"
        else:
            id = "388.l.27081"
        fn = "{}/sample.player_stats.{}.json".format(self.dir_path, id)
        with open(fn, "r") as f:
            return json.load(f)

    def get_draftresults_raw(self, league_id):
        """
        GET draft results for the league

        :param league_id: The league ID that the API request applies to
        :type league_id: str
        :return: Response from the GET call
        """
        fn = "{}/sample.draftresults.{}.json".format(self.dir_path, league_id)
        with open(fn, "r") as f:
            return json.load(f)

    def get_player_raw(self, league_id, search=None, ids=None):
        if search is not None:
            fn = "{}/sample.player_details.{}.json".format(self.dir_path,
                                                           search)
        elif ids is not None:
            fn = "{}/sample.player_details.ids.json".format(self.dir_path)
        else:
            assert(False), "Unsupported lookup"
        with open(fn, "r") as f:
            return json.load(f)

    def get_game_raw(self, game_code):
        """Return the raw JSON when requesting details of a game.

        :param game_code: Game code to get the standings for. (nfl,mlb,nba, nhl)
        :type game_code: str
        :return: JSON document of the request.
        """
        with open(self.dir_path + "/sample.game_details.json", "r") as f:
            return json.load(f)

    def get_transactions_raw(self, league_id, tran_types, count):
        """Return the raw JSON when requesting transactions of a league.
        :param league_id: The league ID that the API request applies to
        :type league_id: str
        :param tran_types: The comman seperated types of transactions retrieve.  Valid values
        are: add,drop,commish,trade
        :type tran_types str
        :param count: The number of transactions to retrieve. Leave blank to return all
        transactions
        :type count str
        :return: JSON document of the request.
        """
        with open(self.dir_path + "/sample.transactions.json", "r") as f:
            return json.load(f)
