#!/bin/python

from yahoo_fantasy_api import yhandler, team
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

    def inject_yhandler(self, yhandler):
        self.yhandler = yhandler

    def to_team(self, team_key):
        """Construct a Team object from a League

        :param team_key: Team key of the new Team object to construct
        :type team_key: str
        :return: Fully constructed object
        :rtype: Team
        """
        tm = team.Team(self.sc, team_key)
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
        t = objectpath.Tree(self.yhandler.get_scoreboard_raw(self.league_id))
        return t.execute('$..current_week[0]')

    def end_week(self):
        """Return the ending week number of the league.

        :return: Week number
        :rtype: int

        >>> lg.end_week()
        24
        """
        t = objectpath.Tree(self.yhandler.get_scoreboard_raw(self.league_id))
        return int(t.execute('$..end_week[0]'))

    def week_date_range(self, week):
        """Return the start and end date of a given week.

        :return: Start and end date of the given week
        :rtype: Pair of datetime.date objects

        >>> lg.week_date_range(12)
        (datetime.date(2019, 6, 17), datetime.date(2019, 6, 23))
        """
        t = objectpath.Tree(self.yhandler.get_scoreboard_raw(self.league_id,
                                                             week))
        j = t.execute('$..(week_start,week_end)[0]')
        return (datetime.datetime.strptime(j['week_start'], "%Y-%m-%d").date(),
                datetime.datetime.strptime(j['week_end'], "%Y-%m-%d").date())
