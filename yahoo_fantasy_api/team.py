#!/bin/python

from yahoo_fantasy_api import yahoo_api
import objectpath


class Team:
    def __init__(self, sc, team_key):
        """Class initializer

        :param sc: Session context for oauth
        :type sc: OAuth2 from yahoo_oauth
        :param team_key: Team key identifier to find the matchups for
        :type team_key: str
        """
        self.sc = sc
        self.team_key = team_key

    def matchup(self, week, data_gen=yahoo_api.get_matchup_raw):
        """Return the team of the matchup my team is playing in a given week

        :param week: Week number to find the matchup for
        :type week: int
        :param data_gen: Optional data generation function.  Only used for
           testing purposes to avoid call-outs to Yahoo!  The function accepts
           3 parameters: sc (session context), team_key, week
        :type data_gen: function
        :return: Team key of the opponent

        >>> tm.matchup(3)
        388.l.27081.t.9
        """
        t = objectpath.Tree(data_gen(self.sc, self.team_key, week))
        json = t.execute('$..matchups..(team_key)')
        for k in json:
            if 'team_key' in k:
                this_team_key = k['team_key']
                if this_team_key != self.team_key:
                    return this_team_key
        raise RuntimeError("Could not find opponent")

    def roster(self, week, data_gen=yahoo_api.get_roster_raw):
        """Return the team roster for a given week

        :param week: Week number of the roster to get
        :type week: int
        :param data_gen: Optional data generation function.  Only used for
           testing purposes to avoid call-outs to Yahoo!  The function accepts
           3 parameters: sc (session context), team_key, week
        :type data_gen: function
        :return: Array of players.  Each entry is a dict with the following
        fields: player_id, name, position_type, eligible_positions,
        selected_position

        >>> tm.roster(3)
        [{'player_id': 8578, 'name': 'John Doe', 'position_type': 'B',
         'eligible_positions': ['C','1B'], 'selected_position': 'C'},
         {'player_id': 8967, 'name': 'Joe Baseball', 'position_type': 'B',
         'eligible_positions': ['SS'], 'selected_position': 'SS'},
         {'player_id': 9961, 'name': 'Ed Reliever', 'position_type': 'P',
         'eligible_positions': ['RP']}]
        """
        t = objectpath.Tree(data_gen(self.sc, self.team_key, week))
        it = t.execute('''
                        $..(player_id,full,position_type,eligible_positions,
                            selected_position)''')

        def _compact_selected_pos(j):
            return j["selected_position"][1]["position"]

        def _compact_eligible_pos(j):
            compact_pos = []
            for p in j["eligible_positions"]:
                compact_pos.append(p['position'])
            return compact_pos

        roster = []
        try:
            while True:
                roster.append({"player_id": int(next(it)["player_id"]),
                               "name": next(it)["full"],
                               "position_type": next(it)["position_type"],
                               "eligible_positions":
                               _compact_eligible_pos(next(it)),
                               "selected_position":
                               _compact_selected_pos(next(it))})
        except StopIteration:
            pass
        return roster
