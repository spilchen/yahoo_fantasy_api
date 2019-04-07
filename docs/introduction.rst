Introduction
============

Yahoo! has APIs for it's fantasy service, which are documented at https://developer.yahoo.com/fantasysports/guide/.  The motivation for this package is to provide a convenient front end for these APIs without having to write (a) authentication boilerplate code and (b) code to read and parse the JSON response.  In addition, the Yahoo! APIs provide a *vast* amount of data; this package provides APIs to get at more targeted data and return it in a more consumable format.

This package is structured with a class hierarchy, which offers fantasy information at various abstraction levels:

- At the top level is the ``Game`` class.  A game, in the Yahoo! fantasy sense, is individual leagues you are part of -- both active and historical.
- Next comes the ``League`` class.  This is a particular instance of a game.  It represents a particular season and game code that you played in.   The league is found by its unique league ID.
- Next level down in the hierarchy is the ``Team`` class.  Within a league there are individual teams.  The teams can be your own teams that you owned or one of your opponents.
- Finally at the lowest level are individual players that either exist on a team or are free agents.  There is no `Player` class to represent this level.
