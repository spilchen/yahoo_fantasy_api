#!/bin/python

from yahoo_fantasy_api import yhandler
import objectpath
from xml.dom.minidom import Document


class Team:
    """An abstraction for all of the team-level APIs in Yahoo! fantasy

    :param sc: Fully constructed session context
    :type sc: :class:`yahoo_oauth.OAuth2`
    :param team_key: Team key identifier for the team we are constructing this
        object for.
    :type team_key: str
    """
    def __init__(self, sc, team_key):
        self.sc = sc
        self.team_key = team_key
        self.league_id = team_key[0:team_key.find(".t")]
        self.league_prefix = team_key[0:team_key.find('.')]
        self.yhandler = yhandler.YHandler(sc)

    def inject_yhandler(self, yhandler):
        self.yhandler = yhandler

    def matchup(self, week):
        """Return the team of the matchup my team is playing in a given week

        :param week: Week number to find the matchup for
        :type week: int
        :return: Team key of the opponent

        >>> tm.matchup(3)
        388.l.27081.t.9
        """
        t = objectpath.Tree(self.yhandler.get_matchup_raw(self.team_key, week))
        json = t.execute('$..matchups..(team_key)')
        for k in json:
            if 'team_key' in k:
                this_team_key = k['team_key']
                if this_team_key != self.team_key:
                    return this_team_key
        raise RuntimeError("Could not find opponent")

    def roster(self, week=None, day=None):
        """Return the team roster for a given week or date

        If neither week or day is specified it will return today's roster.

        :param week: Week number of the roster to get
        :type week: int
        :param day: Day to get the roster
        :type day: :class: datetime.date
        :return: Array of players.  Each entry is a dict with the following
           fields: player_id, name, position_type, eligible_positions,
           selected_position

        >>> tm.roster(3)
        [{'player_id': 8578, 'name': 'John Doe', 'position_type': 'B',
         'eligible_positions': ['C','1B'], 'selected_position': 'C',
         'status': ''},
         {'player_id': 8967, 'name': 'Joe Baseball', 'position_type': 'B',
         'eligible_positions': ['SS'], 'selected_position': 'SS',
         'status': 'DTD'},
         {'player_id': 9961, 'name': 'Ed Reliever', 'position_type': 'P',
         'eligible_positions': ['RP'], 'status': ''}]
        """
        t = objectpath.Tree(self.yhandler.get_roster_raw(self.team_key,
                                                         week=week, day=day))
        it = t.execute('''
                        $..(player_id,full,position_type,eligible_positions,
                            selected_position,status)''')

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
                plyr = {"player_id": int(next(it)["player_id"]),
                        "name": next(it)["full"]}
                next_item = next(it)
                plyr["status"] = next_item["status"] \
                    if "status" in next_item else ""
                if plyr["status"] is "":
                    plyr["position_type"] = next_item["position_type"]
                else:
                    plyr["position_type"] = next(it)["position_type"]
                plyr["eligible_positions"] = _compact_eligible_pos(next(it))
                plyr["selected_position"] = _compact_selected_pos(next(it))

                roster.append(plyr)
        except StopIteration:
            pass
        return roster

    def change_positions(self, day, modified_lineup):
        """Change the starting position of a subset of players in your lineup

        This raises a RuntimeError if any error occurs when communicating with
        Yahoo!

        :param day: The day that the new positions take affect.  This should be
        the starting day of the week.
        :type day: :class: datetime.date
        :param modified_lineup: List of players to modify.  Each entry should
        have a dict with the following keys: player_id - player ID of the
        player to change; selected_position - new position of the player.
        :type modified_lineup: list(dict)

        >>>
        import datetime
        cd = datetime.date(2019, 10, 7)
        plyrs = [{'player_id': 5981, 'selected_position': 'BN'},
                 {'player_id': 4558, 'selected_position': 'BN'}]
        tm.change_positions(cd, plyrs)
        """
        xml = self._construct_change_roster_xml(day, modified_lineup)
        self.yhandler.put_roster(self.team_key, xml)

    def add_player(self, player_id):
        """Add a single player by their player ID

        :param player_id: Yahoo! player ID of the player to add
        :type player_id: int

        >>> tm.add_player(6767)
        """
        xml = self._construct_transaction_xml("add", player_id)
        self.yhandler.post_transactions(self.league_id, xml)

    def drop_player(self, player_id):
        """Drop a single player by their player ID

        :param player_id: Yahoo! player ID of the player to drop
        :type player_id: int

        >>> tm.drop_player(6770)
        """
        xml = self._construct_transaction_xml("drop", player_id)
        self.yhandler.post_transactions(self.league_id, xml)

    def add_and_drop_players(self, add_player_id, drop_player_id):
        """Add one player and drop another in the same transaction

        :param add_player_id: Yahoo! player ID of the player to add
        :type add_player_id: int
        :param drop_player_id: Yahoo! player ID of the player to drop
        :type drop_player_id: int

        >>> tm.add_and_drop_players(6770, 6767)
        """
        xml = self._construct_transaction_xml("add/drop", add_player_id,
                                              drop_player_id)
        self.yhandler.post_transactions(self.league_id, xml)

    def _construct_change_roster_xml(self, day, modified_lineup):
        """Construct XML to pass to Yahoo! that will modified the positions"""
        doc = Document()
        roster = doc.appendChild(doc.createElement('fantasy_content')) \
            .appendChild(doc.createElement('roster'))

        roster.appendChild(doc.createElement('coverage_type')) \
            .appendChild(doc.createTextNode('date'))
        roster.appendChild(doc.createElement('date')) \
            .appendChild(doc.createTextNode(day.strftime("%Y-%m-%d")))

        plyrs = roster.appendChild(doc.createElement('players'))
        for plyr in modified_lineup:
            p = plyrs.appendChild(doc.createElement('player'))
            p.appendChild(doc.createElement('player_key')) \
                .appendChild(doc.createTextNode('{}.p.{}'.format(
                    self.league_prefix, int(plyr['player_id']))))
            p.appendChild(doc.createElement('position')) \
                .appendChild(doc.createTextNode(plyr['selected_position']))

        return doc.toprettyxml()

    def _construct_transaction_xml(self, action, *player_ids):
        doc = Document()
        transaction = doc.appendChild(doc.createElement('fantasy_content')) \
            .appendChild(doc.createElement('transaction'))

        transaction.appendChild(doc.createElement('type')) \
            .appendChild(doc.createTextNode(action))
        if action == 'add/drop':
            players = transaction.appendChild(doc.createElement('players'))
            self._construct_transaction_player_xml(doc, players, player_ids[0],
                                                   "add")
            self._construct_transaction_player_xml(doc, players, player_ids[1],
                                                   "drop")
        else:
            self._construct_transaction_player_xml(doc, transaction,
                                                   player_ids[0], action)
        return doc.toprettyxml()

    def _construct_transaction_player_xml(self, doc, root, player_id, action):
        if action == 'add':
            team_elem = 'destination_team_key'
        elif action == 'drop':
            team_elem = 'source_team_key'
        else:
            assert(False), 'Unknown action: ' + action

        player = root.appendChild(doc.createElement('player'))
        player.appendChild(doc.createElement('player_key')) \
            .appendChild(doc.createTextNode('{}.p.{}'.format(
                self.league_prefix, int(player_id))))
        tdata = player.appendChild(doc.createElement('transaction_data'))
        tdata.appendChild(doc.createElement('type')) \
            .appendChild(doc.createTextNode(action))
        tdata.appendChild(doc.createElement(team_elem)) \
            .appendChild(doc.createTextNode(self.team_key))
