================
yahoo_fantasy_ai
================

Python bindings to the Yahoo! Fantasy API

Build status
------------

.. image:: https://travis-ci.com/spilchen/yahoo_fantasy_api.svg?branch=master
    :target: https://travis-ci.com/spilchen/yahoo_fantasy_api

Installation
------------

This package can be installed via pip:

::

  pip install yahoo_fantasy_api


or from the repo:

::

  git clone https://github.com/spilchen/yahoo_fantasy_api
  cd yahoo_fantasy_api
  python setup.py install


Sample API Usage
----------------

::

  In [1]: from yahoo_oauth import OAuth2
  
  In [2]: from yahoo_fantasy_api import league, game, team
  
  In [3]: sc = OAuth2(None, None, from_file='examples/oauth2.json')
  [2019-04-04 20:55:46,745 DEBUG] [yahoo_oauth.yahoo_oauth.__init__] Checking
  [2019-04-04 20:55:46,746 DEBUG] [yahoo_oauth.yahoo_oauth.token_is_valid] ELAPSED TIME : 416.15308594703674
  [2019-04-04 20:55:46,746 DEBUG] [yahoo_oauth.yahoo_oauth.token_is_valid] TOKEN IS STILL VALID
  
  In [4]: gm = game.Game(sc, 'mlb')
  
  In [5]: gm.league_ids(year=2019)
  Out[5]: ['388.l.27081']
  
  In [6]: lg = gm.to_league('388.l.27081') 
  
  In [7]: lg.stat_categories()
  Out[7]:
  [{'display_name': 'R', 'position_type': 'B'},
   {'display_name': 'HR', 'position_type': 'B'},
   {'display_name': 'RBI', 'position_type': 'B'},
   {'display_name': 'SB', 'position_type': 'B'},
   {'display_name': 'AVG', 'position_type': 'B'},
   {'display_name': 'OBP', 'position_type': 'B'},
   {'display_name': 'W', 'position_type': 'P'},
   {'display_name': 'K', 'position_type': 'P'},
   {'display_name': 'HLD', 'position_type': 'P'},
   {'display_name': 'ERA', 'position_type': 'P'},
   {'display_name': 'WHIP', 'position_type': 'P'},
   {'display_name': 'NSV', 'position_type': 'P'}]
  
  In [8]: lg.team_key()
  Out[8]: '388.l.27081.t.5' 
  
  In [9]: tm = lg.to_team('388.l.27081.t.5')
  
  In [9]: tm.roster(1)
  Out[9]:
  [{'player_id': 8578,
    'name': 'Buster Posey',
    'position_type': 'B',
    'eligible_positions': ['C', '1B', 'Util'],
    'selected_position': 'C'},
   {'player_id': 8967,
    'name': 'Paul Goldschmidt',
    'position_type': 'B',
    'eligible_positions': ['1B', 'Util'],
    'selected_position': '1B'},
   {'player_id': 9961,
    'name': 'Travis Shaw',
    'position_type': 'B',
    'eligible_positions': ['1B', '2B', '3B', 'Util'],
    'selected_position': '2B'},
   {'player_id': 9105,
    'name': 'Nolan Arenado',
    'position_type': 'B',
    'eligible_positions': ['3B', 'Util'],
    'selected_position': '3B'},
   {'player_id': 9468,
    'name': 'Jonathan Villar',
    'position_type': 'B',
    'eligible_positions': ['2B', 'SS', 'Util'],
    'selected_position': 'SS'},
   {'player_id': 10626,
    'name': 'Juan Soto',
    'position_type': 'B',
    'eligible_positions': ['LF', 'Util'],
    'selected_position': 'LF'},
   {'player_id': 9320,
    'name': 'Christian Yelich',
    'position_type': 'B',
    'eligible_positions': ['LF', 'CF', 'RF', 'Util'],
    'selected_position': 'CF'},
   {'player_id': 9002,
    'name': 'J.D. Martinez',
    'position_type': 'B',
    'eligible_positions': ['LF', 'RF', 'Util'],
    'selected_position': 'RF'},
   {'player_id': 9561,
    'name': 'Jesse Winker',
    'position_type': 'B',
    'eligible_positions': ['LF', 'RF', 'Util'],
    'selected_position': 'Util'},
   {'player_id': 9048,
    'name': 'Corey Kluber',
    'position_type': 'P',
    'eligible_positions': ['SP'],
    'selected_position': 'SP'},
   {'player_id': 9317,
    'name': 'Hyun-Jin Ryu',
    'position_type': 'P',
    'eligible_positions': ['SP'],
    'selected_position': 'SP'},
   {'player_id': 10941,
    'name': 'Joey Lucchesi',
    'position_type': 'P',
    'eligible_positions': ['SP'],
    'selected_position': 'SP'},
   {'player_id': 10141,
    'name': 'Zach Eflin',
    'position_type': 'P',
    'eligible_positions': ['SP'],
    'selected_position': 'SP'},
   {'player_id': 10185,
    'name': 'Joe Musgrove',
    'position_type': 'P',
    'eligible_positions': ['SP'],
    'selected_position': 'SP'},
   {'player_id': 7847,
    'name': 'Andrew Miller',
    'position_type': 'P',
    'eligible_positions': ['RP'],
    'selected_position': 'RP'},
   {'player_id': 9358,
    'name': 'Ryan Pressly',
    'position_type': 'P',
    'eligible_positions': ['RP'],
    'selected_position': 'RP'},
   {'player_id': 9039,
    'name': 'Brad Peacock',
    'position_type': 'P',
    'eligible_positions': ['RP'],
    'selected_position': 'RP'},
   {'player_id': 9542,
    'name': 'Archie Bradley',
    'position_type': 'P',
    'eligible_positions': ['RP'],
    'selected_position': 'RP'},
   {'player_id': 10105,
    'name': 'Kenta Maeda',
    'position_type': 'P',
    'eligible_positions': ['SP', 'RP'],
    'selected_position': 'RP'},
   {'player_id': 10867,
    'name': 'Shane Bieber',
    'position_type': 'P',
    'eligible_positions': ['SP'],
    'selected_position': 'BN'},
   {'player_id': 10730,
    'name': 'Brandon Woodruff',
    'position_type': 'P',
    'eligible_positions': ['SP', 'RP'],
    'selected_position': 'BN'}]
