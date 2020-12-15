#!/bin/python

import datetime

YAHOO_ENDPOINT = 'https://fantasysports.yahooapis.com/fantasy/v2'


class YHandler:
    """Class that constructs the APIs to send to Yahoo"""

    def __init__(self, sc):
        self.sc = sc

    def get(self, uri):
        """Send an API request to the URI and return the response as JSON

        :param uri: URI of the API to call
        :type uri: str
        :return: JSON document of the response
        :raises: RuntimeError if any response comes back with an error
        """
        response = self.sc.session.get("{}/{}".format(YAHOO_ENDPOINT, uri),
                                       params={'format': 'json'})
        if response.status_code != 200:
            raise RuntimeError(response.content)
        jresp = response.json()
        return jresp

    def put(self, uri, data):
        """Calls the PUT method to the uri with a payload

        :param uri: URI of the API to call
        :type uri: str
        :param data: What to pass as the payload
        :type data: str
        :return: XML document of the response
        :raises: RuntimeError if any response comes back with an error
        """
        headers = {'Content-Type': 'application/xml'}
        response = self.sc.session.put("{}/{}".format(YAHOO_ENDPOINT, uri),
                                       data=data, headers=headers)
        if response.status_code != 200:
            raise RuntimeError(response.content)
        return response

    def post(self, uri, data):
        """Calls the POST method to the URI with a payload

        :param uri: URI of the API to call
        :type uri: str
        :param data: What to pass as the payload
        :type data: str
        :return: XML document of the response
        :raises: RuntimeError if any response comes back with an error
        """
        headers = {'Content-Type': 'application/xml'}
        response = self.sc.session.post("{}/{}".format(YAHOO_ENDPOINT, uri),
                                        data=data, headers=headers)
        if response.status_code != 201:
            raise RuntimeError(response.content)
        return response

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

    def get_roster_raw(self, team_key, week=None, day=None):
        """Return the raw JSON when requesting a team's roster

        Can request a roster for a given week or a given day.  If neither is
        given the current day's roster is returned.

        :param team_key: Team key identifier to find the matchups for
        :type team_key: str
        :param week: What week number to request the roster for?
        :type week: int
        :param day: What day number to request the roster
        :type day: datetime.date
        :return: JSON of the request
        """
        if week is not None:
            param = ";week={}".format(week)
        elif day is not None:
            param = ";date={}".format(day.strftime("%Y-%m-%d"))
        else:
            param = ""
        return self.get("team/{}/roster{}".format(team_key, param))

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

        The result is limited to 25 players.

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
        return self.get(
            "league/{}/players;start={};count=25;status={}{}/percent_owned".
            format(league_id, start, status, pos_parm))

    def get_player_raw(self, league_id, search=None, ids=None):
        """Return the raw JSON when requesting player details

        :param league_id: League ID to get the player for
        :type league_id: str
        :param search: Search string to apply.  This can be a full or partial
            name of a player.  Cannot be used with ids.
        :type search: str
        :param ids: Set of player IDs to lookup.  Cannot be used with search.
        :type ids: list
        :return: JSON document of the request.
        """
        if search is not None:
            assert(ids is None)
            players_uri = "search={}".format(search)
        elif ids is not None and len(ids) > 0:
            assert(search is None)
            # Construct a player key by prefixing the start of the league ID
            lg_pref = league_id[0:league_id.find('.')]
            players_uri = "player_keys=" + ",".join(
                "{}.p.{}".format(lg_pref, i) for i in ids)
        else:
            raise RuntimeError(
                "Must use search or ids options to filter players.")
        return self.get("league/{}/players;{}/stats".format(league_id,
                                                            players_uri))

    def get_percent_owned_raw(self, league_id, player_ids):
        """Return the raw JSON when requesting the percentage owned of players

        :param league_id: League ID we are requesting data from
        :type league_id: str
        :param player_ids: Yahoo! Player IDs to retrieve % owned for
        :type player_ids: list(str)
        :return: JSON document of the request
        """
        lg_pref = league_id[0:league_id.find(".")]
        joined_ids = ",".join([lg_pref + ".p." + str(i) for i in player_ids])
        return self.get(
            "league/{}/players;player_keys={}/percent_owned".
            format(league_id, joined_ids))
    
    def get_player_ownership_raw(self, league_id, player_ids):
        """Return the raw JSON when requesting the ownership of players

        :param league_id: League ID we are requesting data from
        :type league_id: str
        :param player_ids: Yahoo! Player IDs to retrieve % owned for
        :type player_ids: list(int)
        :return: JSON document of the request
        """
        lg_pref = league_id[0:league_id.find(".")]
        joined_ids = ",".join([lg_pref + ".p." + str(i) for i in player_ids])
        return self.get(
            "league/{}/players;player_keys={}/ownership".
            format(league_id, joined_ids))

    def put_roster(self, team_key, xml):
        """Calls PUT against the roster API passing it an xml document

        :param team_key: The key of the team the roster move applies too
        :type team_key: str
        :param xml: The XML document to send
        :type xml: str
        :return: Response from the PUT
        """
        return self.put("team/{}/roster".format(team_key), xml)

    def post_transactions(self, league_id, xml):
        """Calls POST against the transaction API passing it an xml document

        :param league_id: The league ID that the API request applies to
        :type league_id: str
        :param xml: The XML document to send as the payload
        :type xml: str
        :return: Response from the POST
        """
        return self.post("league/{}/transactions".format(league_id), xml)

    def get_team_transactions(self, league_id, team_key, tran_type):
        """
        Calls GET to retrieve transactions for a team of a given type.

        :param league_id: The league ID that the API request applies to
        :type league_id: str
        :param team_key: The key of the team the roster move applies too
        :type team_key: str
        :param tran_type: The type of transaction retrieve.  Valid values
        are: waiver or pending_trade
        :return: Response from the GET
        """
        return self.get(
            "league/{}/transactions;team_key={};type={}".format(
                league_id, team_key, tran_type))

    def get_transactions_raw(self, league_id, tran_types, count):
        """
        Calls GET to retrieve transactions of a given type.

        :param league_id: The league ID that the API request applies to
        :type league_id: str
        :param tran_types: The comman seperated types of transactions retrieve.  Valid values
        are: add,drop,commish,trade
        :type tran_types str
        :param count: The number of transactions to retrieve. Leave blank to return all
        transactions
        :type count str
        :return: Response from the GET
        """
        return self.get(
            "league/{}/transactions;types={};count={}".format(
                league_id, tran_types, count))

    def put_transaction(self, transaction_key, xml):
        """
        PUT to the transaction API

        This can be used to accept/reject trades, voting for/against a trade,
        and editing a waiver claim.

        :param xml: The XML document to send
        :type xml: str
        :return: Response from the PUT
        """
        return self.put("transaction/" + str(transaction_key), xml)

    def get_player_stats_raw(self, game_code, player_ids, req_type, date,
                             season):
        """
        GET stats for a list of player IDs

        :param game_code: The game code the players belong too.  mlb, nhl, etc.
        :type game_code: str
        :param player_ids: Yahoo! player IDs we are requesting stats for
        :type player_ids: list(int)
        :param req_type: The request type.  This defines the range of dates to
            return the stats for.
        :param date: When req_type == 'date', this is the date we want the
            stats for.  If None, we'll get the stats for the current date.
        :type date: datetime.date
        :param season: When req_type == 'season', this is the season we want
            the stats for.  If None, we'll get the stats for the current season
        :type season: int
        :return: Response from the GET call
        """
        uri = self._build_player_stats_uri(game_code, player_ids, req_type,
                                           date, season)
        return self.get(uri)

    def get_draftresults_raw(self, league_id):
        """
        GET draft results for the league

        :param league_id: The league ID that the API request applies to
        :type league_id: str
        :return: Response from the GET call
        """
        return self.get("league/{}/draftresults".format(league_id))

    def _build_player_stats_uri(self, game_code, player_ids, req_type, date,
                                season):
        uri = 'players;player_keys='
        if type(player_ids) is list:
            for i, p in enumerate(player_ids):
                if i != 0:
                    uri += ","
                uri += "{}.p.{}".format(game_code, p)
        uri += "/stats;{}".format(self._get_stats_type(req_type, date, season))
        return uri

    def _get_stats_type(self, req_type, date, season):
        if req_type == 'season':
            if season is None:
                return "type=season"
            else:
                return "type=season;season={}".format(season)
        elif req_type == 'date':
            if date is None:
                date = datetime.date.today()
            if type(date) is datetime.date or type(date) is datetime.datetime:
                return "type=date;date={}".format(date.strftime("%Y-%m-%d"))
            else:
                return "type=date;date={}".format(date)
        elif req_type in ['lastweek', 'lastmonth']:
            return "type={}".format(req_type)
        else:
            assert(False), "Unknown req_type type: {}".format(req_type)

    def get_game_raw(self, game_code):
        """Return the raw JSON when requesting details of a game.

        :param game_code: Game code to get the standings for. (nfl,mlb,nba, nhl)
        :type game_code: str
        :return: JSON document of the request.
        """
        return self.get("game/{}".format(game_code))
