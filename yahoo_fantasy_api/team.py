#!/bin/python

from yahoo_fantasy_api import yhandler
import objectpath
import datetime
from xml.dom.minidom import Document

from yahoo_fantasy_api.utils import create_element


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

    def details(self):
        """Return the details of the team

        :return: Dictionary of the team details

        >>> tm.details()
        {'team_key': '388.l.27081.t.9', 'team_id': '9', 'name': 'Team Name',
         'url': 'http://baseball.fantasysports.yahoo.com/archive/mlb/2013/27081/9',
         'team_logos': [{'team_logo': {'size': 'large', 'url': 'http://l.yimg
        """
        t = objectpath.Tree(self.yhandler.get_teams_by_keys_raw([self.team_key]))
        json = t.execute('$..teams..team[0]')
        details = {k: v for dic in [val for val in json if val != []] for k, v in dic.items()}
        return details

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
        raw = self.yhandler.get_roster_raw(self.team_key, week=week, day=day)
        t = objectpath.Tree(raw)
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
                plyr["status"] = next_item["status"]
                # The query we use to pick out only certain fields will find
                # one or two fields named status.  One 'status' field that will
                # always exist is for keeper info -- we don't care about that
                # one.  We only care about the 'status' field that tells if
                # they are on the IL, DTD, etc.  But this isn't there if the
                # player has a clean bill of health.  We tell if its the status
                # we don't care about by looking at the type; bool means it is
                # for keeper info.
                if isinstance(plyr["status"], bool):
                    plyr["status"] = ""
                else:
                    # Burn the next field as its the keeper info we don't care about
                    next(it)
                plyr["position_type"] = next(it)["position_type"]
                plyr["eligible_positions"] = _compact_eligible_pos(next(it))
                plyr["selected_position"] = _compact_selected_pos(next(it))

                roster.append(plyr)
        except StopIteration:
            pass
        return roster

    def change_positions(self, time_frame, modified_lineup):
        """Change the starting position of a subset of players in your lineup

        This raises a RuntimeError if any error occurs when communicating with
        Yahoo!

        :param time_frame: The time frame that the new positions take affect.  This should be
            the starting day of the week (MLB, NBA, or NHL) or the week number (NFL).
        :type time_frame: :class:`datetime.date` | int
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
        xml = self._construct_change_roster_xml(time_frame, modified_lineup)
        self.yhandler.put_roster(self.team_key, xml)

    def add_player(self, player_id):
        """Add a single player by their player ID

        :param player_id: Yahoo! player ID of the player to add
        :type player_id: int

        >>> tm.add_player(6767)
        """
        xml = self._construct_transaction_xml("add", player_id)
        self.yhandler.post_transactions(self.league_id, xml)

    def claim_player(self, player_id, faab=None):
        """Submit a waiver claim for a single player by their player ID

        :param player_id: Yahoo! player ID of the player to add
        :type player_id: int
        :param faab: Number of faab dollars to bid on the claim
        :type faab: int

        >>> tm.add_player(6767, faab=7)
        """
        xml = self._construct_transaction_xml("add", player_id, faab=faab)
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

    def claim_and_drop_players(self, add_player_id, drop_player_id, faab=None):
        """Submit a waiver claim for one player and drop another in the same transaction

        :param add_player_id: Yahoo! player ID of the player to add
        :type add_player_id: int
        :param drop_player_id: Yahoo! player ID of the player to drop
        :type drop_player_id: int
        :param faab: Number of faab dollars to bid on the claim
        :type faab: int

        >>> tm.claim_and_drop_players(6770, 6767, faab=22)
        """
        xml = self._construct_transaction_xml(
            "add/drop", add_player_id, drop_player_id, faab=faab
        )
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

    def propose_trade(self, tradee_team_key: str, players: list[dict[str, str]],
                      trade_note: str = "") -> None:
        """
        Propose a trade

        :param tradee_team_key: Team key of the team receiving the trade
        :type tradee_team_key: str
        :param players: List of players to trade.  Each entry should have a
            dict with the following keys: player_key - player key of the
            player to trade; source_team_key - team key of the team that
            currently owns the player; destination_team_key - team key of the
            team that will receive the player.
        :type players: list(dict)
        :param trade_note: Optional note to include with the trade
        :type trade_note: str
        """
        xml = self._construct_trade_proposal_xml(tradee_team_key, players, trade_note)
        self.yhandler.post_transactions(self.league_id, xml)

    def _construct_trade_xml(self, transaction_key: str, action: str, trade_note: str) -> str:
        """Construct trade XML
        :param transaction_key: Key of the transaction

        :type transaction_key: str

        :param action: Action to be performed

        :type action: str

        :param trade_note: Note to include with the trade

        :type trade_note: str

        :return: XML representation of the trade
        :rtype: str
        """
        doc = Document()
        tran = doc.createElement('transaction')
        doc.appendChild(doc.createElement('fantasy_content')).appendChild(tran)

        create_element(doc, tran, 'transaction_key', transaction_key)
        create_element(doc, tran, 'type', 'pending_trade')
        create_element(doc, tran, 'action', action)
        create_element(doc, tran, 'trade_note', trade_note)

        return doc.toprettyxml()

    def _construct_trade_proposal_xml(self, tradee_team_key: str, your_player_keys: list[str],
                                      their_players_keys: list[str], trade_note: str = "") -> str:
        """
        Constructs a trade proposal XML.

        :param tradee_team_key: Key of the team to trade with.
        :type tradee_team_key: str

        :param your_player_keys: List of keys of your players involved in the trade.
        :type your_player_keys: list[str]

        :param their_players_keys: List of keys of the other team's players involved in the trade.
        :type their_players_keys: list[str]

        :param trade_note: Note to include with the trade. Default is an empty string.
        :type trade_note: str

        :return: XML representation of the trade proposal.
        :rtype: str
        """
        doc = Document()
        transaction = doc.createElement('transaction')
        doc.appendChild(doc.createElement('fantasy_content')).appendChild(transaction)

        create_element(doc, transaction, 'type', 'pending_trade')
        create_element(doc, transaction, 'trader_team_key', self.team_key)
        create_element(doc, transaction, 'tradee_team_key', tradee_team_key)
        create_element(doc, transaction, 'trade_note', trade_note)

        players_element = doc.createElement('players')
        transaction.appendChild(players_element)

        your_players = [
            {"player_key": player_key, "source_team_key": self.team_key, "destination_team_key": tradee_team_key}
            for player_key in your_player_keys]
        their_players = [
            {"player_key": player_key, "source_team_key": tradee_team_key, "destination_team_key": self.team_key}
            for player_key in their_players_keys]

        players = your_players + their_players

        for player in players:
            player_element = doc.createElement('player')
            players_element.appendChild(player_element)

            create_element(doc, player_element, 'player_key', player['player_key'])

            transaction_data = doc.createElement('transaction_data')
            player_element.appendChild(transaction_data)

            create_element(doc, transaction_data, 'type', 'pending_trade')
            create_element(doc, transaction_data, 'source_team_key', player['source_team_key'])
            create_element(doc, transaction_data, 'destination_team_key', player['destination_team_key'])

        return doc.toprettyxml()

    def _construct_change_roster_xml(self, time_frame, modified_lineup):
        """Construct XML to pass to Yahoo! that will modified the positions"""
        doc = Document()
        roster = doc.appendChild(doc.createElement('fantasy_content')) \
            .appendChild(doc.createElement('roster'))

        if isinstance(time_frame, datetime.date):
            roster.appendChild(doc.createElement('coverage_type')) \
                .appendChild(doc.createTextNode('date'))
            roster.appendChild(doc.createElement('date')) \
                .appendChild(doc.createTextNode(time_frame.strftime("%Y-%m-%d")))
        elif isinstance(time_frame, int):
            roster.appendChild(doc.createElement('coverage_type')) \
                .appendChild(doc.createTextNode('week'))
            roster.appendChild(doc.createElement('week')) \
                .appendChild(doc.createTextNode(str(time_frame)))
        else:
            raise RuntimeError("Invalid time_frame format. Must be datetime.date or int.")

        plyrs = roster.appendChild(doc.createElement('players'))
        for plyr in modified_lineup:
            p = plyrs.appendChild(doc.createElement('player'))
            p.appendChild(doc.createElement('player_key')) \
                .appendChild(doc.createTextNode('{}.p.{}'.format(
                    self.league_prefix, int(plyr['player_id']))))
            p.appendChild(doc.createElement('position')) \
                .appendChild(doc.createTextNode(plyr['selected_position']))

        return doc.toprettyxml()

    def _construct_transaction_xml(self, action, *player_ids, faab=None):
        doc = Document()
        transaction = doc.appendChild(doc.createElement('fantasy_content')) \
            .appendChild(doc.createElement('transaction'))

        transaction.appendChild(doc.createElement('type')) \
            .appendChild(doc.createTextNode(action))

        if faab is not None:
            transaction.appendChild(doc.createElement("faab_bid")) \
                .appendChild(doc.createTextNode(str(faab)))

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
            assert (False), 'Unknown action: ' + action

        player = root.appendChild(doc.createElement('player'))
        player.appendChild(doc.createElement('player_key')) \
            .appendChild(doc.createTextNode('{}.p.{}'.format(
                self.league_prefix, int(player_id))))
        tdata = player.appendChild(doc.createElement('transaction_data'))
        tdata.appendChild(doc.createElement('type')) \
            .appendChild(doc.createTextNode(action))
        tdata.appendChild(doc.createElement(team_elem)) \
            .appendChild(doc.createTextNode(self.team_key))
