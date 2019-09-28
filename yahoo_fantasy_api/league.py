#!/bin/python

import yahoo_fantasy_api as yfa
from yahoo_fantasy_api import yhandler
import objectpath
import datetime


class League:
    """An abstraction for all of the league-level APIs in Yahoo! fantasy

    :param sc: Fully constructed session context
    :type sc: :class:`yahoo_oauth.OAuth2`
    :param league_id: League ID to setup this class for.  All API requests
        will be for this league.
    :type league_id: str
    """
    def __init__(self, sc, league_id):
        self.sc = sc
        self.league_id = league_id
        self.yhandler = yhandler.YHandler(sc)
        self.current_week_cache = None
        self.end_week_cache = None
        self.week_date_range_cache = {}
        self.free_agent_cache = {}

    def inject_yhandler(self, yhandler):
        self.yhandler = yhandler

    def to_team(self, team_key):
        """Construct a Team object from a League

        :param team_key: Team key of the new Team object to construct
        :type team_key: str
        :return: Fully constructed object
        :rtype: Team
        """
        tm = yfa.Team(self.sc, team_key)
        tm.inject_yhandler(self.yhandler)
        return tm

    def standings(self):
        """Return the standings of the league id

        :return: An ordered list of the teams in the standings.  First entry is
            the first place team.
        :rtype: List

        >>> lg.standings()
        ['Liz & Peter's Twins', 'Lumber Kings', 'Proj. Matt Carpenter']
        """
        json = self.yhandler.get_standings_raw(self.league_id)
        team_json = \
            json['fantasy_content']["league"][1]["standings"][0]["teams"]
        standings = []
        for i in range(team_json["count"]):
            team = team_json[str(i)]["team"][0]
            standings.append(team[2]['name'])
        return standings

    def teams(self):
        """Return a name and key of each team in the league

        :return: A list of teams, each team will have its name and key
        :rtype: List

        >>> lg.teams()
        [{'name': 'Lumber Kings', 'team_key': '370.l.56877.t.5'},
         {'name': 'Roster Sabotage', 'team_key': '370.l.56877.t.6'},
         {'name': 'Springfield Isotopes', 'team_key': '370.l.56877.t.7'}]
        """
        json = self.yhandler.get_standings_raw(self.league_id)
        t = objectpath.Tree(json)
        elems = t.execute('$..teams..(name)')
        teams = []
        for ele in elems:
            teams.append(ele)
        for team, ele in zip(teams, t.execute('$..teams..(team_key)')):
            team['team_key'] = ele['team_key']
        return teams

    def matchups(self):
        """Retrieve matchups data for current week

        :return: Matchup details as key/value pairs
        :rtype: dict
        """
        json = self.yhandler.get_scoreboard_raw(self.league_id)
        return json

    def settings(self):
        """Return the league settings

        :return: League settings as key/value pairs
        :rtype: Dict

        >>> lg.setings()
        {'name': "Buck you're next!", 'scoring_type': 'head',
        'start_week': '1', 'current_week': 1, 'end_week': '24',
        'start_date': '2019-03-20', 'end_date': '2019-09-22',
        'game_code': 'mlb', 'season': '2019'}
        """
        json = self.yhandler.get_settings_raw(self.league_id)
        t = objectpath.Tree(json)
        settings_to_return = """
        name, scoring_type,
        start_week, current_week, end_week,start_date, end_date,
        game_code, season
        """
        return t.execute('$.fantasy_content.league.({})[0]'.format(
            settings_to_return))

    def stat_categories(self):
        """Return the stat categories for a league

        :returns: Each dict entry will have the stat name along
            with the position type ('B' for batter or 'P' for pitcher).
        :rtype: List(Dict)

        >>> lg.stat_categories('370.l.56877')
        [{'display_name': 'R', 'position_type': 'B'}, {'display_name': 'HR',
        'position_type': 'B'}, {'display_name': 'W', 'position_type': 'P'}]
        """
        t = objectpath.Tree(self.yhandler.get_settings_raw(self.league_id))
        json = t.execute('$..stat_categories..stat')
        simple_stat = []
        for s in json:
            # Omit stats that are only for display purposes
            if 'is_only_display_stat' not in s:
                simple_stat.append({"display_name": s["display_name"],
                                    "position_type": s["position_type"]})
        return simple_stat

    def team_key(self):
        """Return the team_key for logged in users team in this league

        :return: The team key
        :rtype: str

        >>> lg.team_key()
        388.l.27081.t.5
        """
        t = objectpath.Tree(self.yhandler.get_teams_raw())
        json = t.execute('$..(team_key)')
        for t in json:
            if t['team_key'].startswith(self.league_id):
                return t['team_key']

    def current_week(self):
        """Return the current week number of the league

        :return: Week number
        :rtype: int

        >>> lg.current_week()
        12
        """
        if self.current_week_cache is None:
            t = objectpath.Tree(self.yhandler.get_scoreboard_raw(
                self.league_id))
            self.current_week_cache = int(t.execute('$..current_week[0]'))
        return self.current_week_cache

    def end_week(self):
        """Return the ending week number of the league.

        :return: Week number
        :rtype: int

        >>> lg.end_week()
        24
        """
        if self.end_week_cache is None:
            t = objectpath.Tree(
                self.yhandler.get_scoreboard_raw(self.league_id))
            self.end_week_cache = int(t.execute('$..end_week[0]'))
        return self.end_week_cache

    def week_date_range(self, week):
        """Return the start and end date of a given week.

        Can only request the date range at most one week in the future.  This
        restriction exists because Yahoo! only provides the week range when the
        matchups are known.  And during the playoffs, the matchup is only known
        for the current week.  A RuntimeError exception is returned if a
        request is for a week too far in the future.

        :return: Start and end date of the given week
        :rtype: Pair of datetime.date objects

        >>> lg.week_date_range(12)
        (datetime.date(2019, 6, 17), datetime.date(2019, 6, 23))
        """
        if week <= self.current_week() or week == 1:
            return self._date_range_of_played_or_current_week(week)
        elif week == self.current_week() + 1:
            (cur_st, cur_end) = self._date_range_of_played_or_current_week(
                week - 1)
            req_st = cur_end + datetime.timedelta(days=1)
            req_end = cur_end + datetime.timedelta(days=7)
            return (req_st, req_end)
        else:
            raise RuntimeError("Cannot request date range more than one week "
                               "past the current week.  The requested week is "
                               "{}, but current week is {}.".format(
                                   week, self.current_week()))

    def free_agents(self, position):
        """Return the free agents for the given position

        :param position: All free agents must be able to play this position.
             Use the short code of the position (e.g. 2B, C, etc.).  You can
             also specify the position type (e.g. 'B' for all batters and 'P'
             for all pitchers).
        :type position: str
        :return: Free agents found. Particulars about each free agent will be
             returned.
        :rtype: List(Dict)

        >>> fa_CF = lg.free_agents('CF')
        >>> len(fa_CF)
        60
        >>> fa_CF[0]
        {'player_id': 8370,
         'name': 'Dexter Fowler',
         'position_type': 'B',
         'eligible_positions': ['CF', 'RF', 'Util']}
        """
        if position not in self.free_agent_cache:
            self._cache_free_agents(position)
        return self.free_agent_cache[position]

    def _cache_free_agents(self, position):
        # The Yahoo! API we use doles out players 25 per page.  We need to make
        # successive calls to gather all of the players.  We stop when we fetch
        # less then 25.
        PLAYERS_PER_PAGE = 25
        self.free_agent_cache[position] = []
        plyrIndex = 0
        while plyrIndex % PLAYERS_PER_PAGE == 0:
            j = self.yhandler.get_players_raw(self.league_id, plyrIndex, 'A',
                                              position=position)
            (num_plyrs_on_pg, fa_on_pg) = self._free_agents_from_page(j)
            self.free_agent_cache[position] += fa_on_pg
            plyrIndex += num_plyrs_on_pg

    def _free_agents_from_page(self, page):
        """Extract the free agents from a given JSON page

        :param page: JSON page to extract free agents from
        :type page: dict
        :return: A tuple returning the number of players on the page, and the
        list of free agents extracted from the page.
        :rtype: (int, list(dict))
        """
        fa = []
        t = objectpath.Tree(page)
        for i in range(t.execute('$..players.count[0]')):
            path = '$..players..player[{}].'.format(i) + \
                "(name,player_id,position_type,status,eligible_positions)"
            obj = list(t.execute(path))
            plyr = {}
            # Convert obj from a list of dicts to a single one-dimensional dict
            for ele in obj:
                for k in ele.keys():
                    plyr[k] = ele[k]
            plyr['player_id'] = int(plyr['player_id'])
            plyr['name'] = plyr['name']['full']
            # We want to return eligible positions in a concise format.
            plyr['eligible_positions'] = [e['position'] for e in
                                          plyr['eligible_positions']]

            # Ignore players that are not active or on the disabled list
            if "status" not in plyr or plyr['status'] == 'DTD':
                fa.append(plyr)
        return (i + 1, fa)

    def _date_range_of_played_or_current_week(self, week):
        """Get the date range of a week that was already played or the current

        Assumes caller has already verified the week is no greater then
        current.

        :param week: Week to request
        :return: Start and end date of the given week
        :rtype: Pair of datetime.date objects
        """
        if week not in self.week_date_range_cache:
            t = objectpath.Tree(self.yhandler.get_scoreboard_raw(
                self.league_id, week))
            j = t.execute('$..(week_start,week_end)[0]')
            self.week_date_range_cache[week] = (
                datetime.datetime.strptime(j['week_start'], "%Y-%m-%d").date(),
                datetime.datetime.strptime(j['week_end'], "%Y-%m-%d").date())
        return self.week_date_range_cache[week]

    def player_details(self, player_name):
        """Retrieve details about a specific player

        :parm player_name: Name of the player to get details for
        :type player_name: str
        :return: Player details
        :rtype: dict
        >>> lg.player_details("Antonio Brown")
        {
            'bye_weeks': {'week': '6'},
            'display_position': 'WR',
            'editorial_player_key': 'nfl.p.24171',
            'editorial_team_abbr': 'Oak',
            'editorial_team_full_name': 'Oakland Raiders',
            'editorial_team_key': 'nfl.t.13',
            'eligible_positions': [{...}, {...}],
            'has_player_notes': 1,
            'has_recent_player_notes': 1,
            'headshot': {
                'size': 'small',
                'url': 'https://s.yimg.com/...24171.png'},
            'image_url': 'https://s.yimg.com/...24171.png',
            'is_undroppable': '1',
            'name': {
                'ascii_first': 'Antonio',
                'ascii_last': 'Brown',
                'first': 'Antonio',
                'full': 'Antonio Brown',
                'last': 'Brown'},
            'player_id': '24171', ...}
        """
        json_query = '$..players'
        t = objectpath.Tree(self.yhandler.get_player_raw(self.league_id,
                                                         player_name))
        json = t.execute(json_query)
        player_data = {}
        for player in json:
            for category in player['0']['player']:
                for sub_category in category:
                    if isinstance(sub_category, str):
                        player_data[sub_category] = category[sub_category]
                    if isinstance(sub_category, dict):
                        for key, value in sub_category.items():
                            player_data[key] = value
            return player_data
