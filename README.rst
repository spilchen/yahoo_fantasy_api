=================
yahoo_fantasy_api
=================

Python bindings to the Yahoo! Fantasy API

Build status
------------

.. image:: https://travis-ci.com/spilchen/yahoo_fantasy_api.svg?branch=master
    :target: https://travis-ci.com/spilchen/yahoo_fantasy_api
    
.. image:: https://readthedocs.org/projects/yahoo-fantasy-api/badge/?version=latest
   :target: https://yahoo-fantasy-api.readthedocs.io/en/latest/?badge=latest
   :alt: Documentation Status

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

Documentation
-------------

The documentation are hosted at readthedocs.io: https://yahoo-fantasy-api.readthedocs.io/en/latest/

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

  In [9]: lg.current_week()
  Out[9]: 12

  In [10]: lg.end_week()
  Out[10]: 24

  In [11]: lg.week_date_range(12)
  Out[11]: (datetime.date(2019, 6, 17), datetime.date(2019, 6, 23))
  
  In [12]: tm = lg.to_team('388.l.27081.t.5')
  
  In [13]: tm.roster(1)
  Out[13]:
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
   ...
   {'player_id': 7847,
    'name': 'Andrew Miller',
    'position_type': 'P',
    'eligible_positions': ['RP'],
    'selected_position': 'RP'}]
