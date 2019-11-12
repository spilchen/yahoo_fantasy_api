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
        :type day: :class:`datetime.date`
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

    def proposed_trades(self):
        """
        Retrieve information for any proposed trades that include your team

        :return: List of proposed trade transactions that you have offered and
            have been offered to you.

        >>> tm.proposed_trades()
        [{'transaction_key': '396.l.49770.pt.1',
          'status': 'proposed',
          'trader_team_key': '396.l.49770.t.4',
          'tradee_team_key': '396.l.49770.t.5',
          'trader_players': [{'player_id': '4472',
            'name': 'Drew Doughty',
            'position_type': 'P'}],
          'tradee_players': [{'player_id': '5689',
            'name': 'Jacob Trouba',
            'position_type': 'P'}]},
         {'transaction_key': '396.l.49770.pt.2',
          'status': 'proposed',
          'trader_team_key': '396.l.49770.t.4',
          'tradee_team_key': '396.l.49770.t.3',
          'trader_players': [{'player_id': '4002',
            'name': 'Claude Giroux',
            'position_type': 'P'},
         {'player_id': '3798', 'name': 'Tuukka Rask', 'position_type': 'G'}],
          'tradee_players': [{'player_id': '5981',
          'name': 'Aleksander Barkov',
          'position_type': 'P'},
         {'player_id': '4685', 'name': 'Brayden Schenn',
           'position_type': 'P'}]}],
         {'transaction_key': '396.l.49770.pt.3',
          'status': 'proposed',
          'trader_team_key': '396.l.49770.t.2',
          'tradee_team_key': '396.l.49770.t.4',
          'trader_players': [{'player_id': '5987',
            'name': 'Rasmus Ristolainen', 'position_type': 'P'}],
          'tradee_players': [{'player_id': '4064',
            'name': 'Kris Letang', 'position_type': 'P'}]}]
        """
        j = self.yhandler.get_team_transactions(self.league_id, self.team_key,
                                                "pending_trade")
        t = objectpath.Tree(j)
        trans = []
        trans_it = t.execute('''$..transaction.(transaction_key,
                                                status,
                                                trader_team_key,
                                                tradee_team_key)''')
        for i, tran in enumerate(trans_it):
            tran["trader_players"] = []
            tran["tradee_players"] = []

            def append_player(plyr):
                """Helper to append a player to proper team list"""
                trader_tm = plyr["source_team_key"] == tran["trader_team_key"]
                del plyr["source_team_key"]
                if trader_tm:
                    tran["trader_players"].append(plyr)
                else:
                    tran["tradee_players"].append(plyr)

            plyr_it = t.execute('''
                $..transactions.'{}'..(player_id,full,position_type,
                                      source_team_key)'''.format(i))
            key_mapper = {"full": "name"}
            plyr = {}
            for elem in plyr_it:
                for key, value in elem.items():
                    if key in plyr:
                        append_player(plyr)
                        plyr = {}
                    if key in key_mapper:
                        plyr[key_mapper[key]] = value
                    else:
                        plyr[key] = value
            append_player(plyr)
            trans.append(tran)
        return trans

    def reject_trade(self, transaction_key, trade_note=""):
        """
        Reject a proposed trade

        :param transaction_key: Transction to reject.  This key is taken from
            the output of the proposed_trades() API.
        :type transaction_key: str
        """
        xml = self._construct_trade_xml(transaction_key, "reject", trade_note)
        self.yhandler.put_transaction(transaction_key, xml)

    def accept_trade(self, transaction_key, trade_note=""):
        """
        Accept a proposed trade

        :param transaction_key: Transction to accept.  This key is taken from
            the output of the proposed_trades() API.
        :type transaction_key: str
        """
        xml = self._construct_trade_xml(transaction_key, "accept", trade_note)
        self.yhandler.put_transaction(transaction_key, xml)

    def _construct_trade_xml(self, transaction_key, action, trade_note):
        doc = Document()
        tran = doc.appendChild(doc.createElement('fantasy_content')) \
            .appendChild(doc.createElement('transaction'))

        tran.appendChild(doc.createElement('transaction_key')) \
            .appendChild(doc.createTextNode(transaction_key))
        tran.appendChild(doc.createElement('type')) \
            .appendChild(doc.createTextNode('pending_trade'))
        tran.appendChild(doc.createElement('action')) \
            .appendChild(doc.createTextNode(action))
        tran.appendChild(doc.createElement('trade_note')) \
            .appendChild(doc.createTextNode(trade_note))
        return doc.toprettyxml()

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
