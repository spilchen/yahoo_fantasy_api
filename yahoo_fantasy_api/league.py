#!/bin/python

from yahoo_fantasy_api import yahoo_api, team
import objectpath


class League:
    def __init__(self, sc, league_id):
        """Class initializer

        :param sc: Session context for oauth
        :type sc: OAuth2 from yahoo_oauth
        :param league_id: League ID to setup this class for.  All API requests
            will be for this league.
        :type code: str.
        """
        self.sc = sc
        self.league_id = league_id

    def to_team(self, team_key):
        """Construct a Team object from a League

        :param team_key: Team key of the new Team object to construct
        :type team_key: str
        :return: Team object
        """
        return team.Team(self.sc, team_key)

    def standings(self, data_gen=yahoo_api.get_standings_raw):
        """Return the standings of the league id

        :param data_gen: Optional data generation function.  This exists for
            test purposes so that we don't have to call-out to Yahoo!
        :type data_type: Function
        :return: An ordered list of the teams in the standings.  First entry is
            the first place team.

        >>> lg.standings()
        ['Liz & Peter's Twins', 'Lumber Kings', 'Proj. Matt Carpenter']
        """
        json = data_gen(self.sc, self.league_id)
        team_json = \
            json['fantasy_content']["league"][1]["standings"][0]["teams"]
        standings = []
        for i in range(team_json["count"]):
            team = team_json[str(i)]["team"][0]
            standings.append(team[2]['name'])
        return standings

    def settings(self, data_gen=yahoo_api.get_settings_raw):
        """Return the league settings

        :param data_gen: Optional data generation function.  This exists for
            test purposes so that we don't have to call-out to Yahoo!
        :type data_type: Function

        >>> lg.setings()
        {'name': "Buck you're next!", 'scoring_type': 'head',
        'start_week': '1', 'current_week': 1, 'end_week': '24',
        'start_date': '2019-03-20', 'end_date': '2019-09-22',
        'game_code': 'mlb', 'season': '2019'}
        """
        json = data_gen(self.sc, self.league_id)
        t = objectpath.Tree(json)
        settings_to_return = """
        name, scoring_type,
        start_week, current_week, end_week,start_date, end_date,
        game_code, season
        """
        return t.execute('$.fantasy_content.league.({})[0]'.format(
            settings_to_return))

    def stat_categories(self, data_gen=yahoo_api.get_settings_raw):
        """Return the stat categories for a league

        :param data_gen: Optional data generation function.  Only used for
           testing purposes to avoid call-outs to Yahoo!
        :type data_gen: function
        :returns: An array of dicts.  Each dict will have the stat name along
            with the position type ('B' for batter or 'P' for pitcher).

        >>> lg.stat_categories('370.l.56877')
        [{'display_name': 'R', 'position_type': 'B'}, {'display_name': 'HR',
        'position_type': 'B'}, {'display_name': 'W', 'position_type': 'P'}]
        """
        t = objectpath.Tree(data_gen(self.sc, self.league_id))
        json = t.execute('$..stat_categories..stat')
        simple_stat = []
        for s in json:
            # Omit stats that are only for display purposes
            if 'is_only_display_stat' not in s:
                simple_stat.append({"display_name": s["display_name"],
                                    "position_type": s["position_type"]})
        return simple_stat

    def team_key(self, data_gen=yahoo_api.get_teams_raw):
        """Return the team_key for logged in users team in this league

        :param data_gen: Optional data generation function.  Only used for
           testing purposes to avoid call-outs to Yahoo!
        :type data_gen: function

        >>> lg.team_key
        388.l.27081.t.5
        """
        t = objectpath.Tree(data_gen(self.sc))
        json = t.execute('$..(team_key)')
        for t in json:
            if t['team_key'].startswith(self.league_id):
                return t['team_key']
