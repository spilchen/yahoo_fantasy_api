#!/bin/python

from yahoo_fantasy_api import yhandler
from unittest.mock import MagicMock, Mock, patch
import datetime
import json


def test_matchup(mock_team):
    opponent = mock_team.matchup(3)
    assert(opponent == '388.l.27081.t.5')


def test_roster_raw():
    yh = yhandler.YHandler('dummy-sc')
    yh.get = MagicMock(return_value=None)
    team_key = '1234'
    yh.get_roster_raw(team_key, week=10)
    yh.get.assert_called_with("team/{}/roster;week=10".format(team_key))
    yh.get_roster_raw(team_key, day=datetime.date(2019, 10, 7))
    yh.get.assert_called_with("team/{}/roster;date=2019-10-07".format(
        team_key))
    yh.get_roster_raw(team_key)
    yh.get.assert_called_with("team/{}/roster".format(team_key))


def test_game_raw():
    yh = yhandler.YHandler('dummy-sc')
    yh.get = MagicMock(return_value=None)
    game_code = "nfl"
    yh.get_game_raw(game_code)
    yh.get.assert_called_with("game/{}".format(game_code))


def test_player_ownership_raw():
    yh = yhandler.YHandler('dummy-sc')
    yh.get = MagicMock(return_value=None)
    league_id = "399.l.710921"
    player_ids = [9265]
    joined_ids = ",".join(["399.p." + str(i) for i in player_ids])
    yh.get_player_ownership_raw(league_id, player_ids)
    yh.get.assert_called_with("league/{}/players;player_keys={}/ownership".format(league_id, joined_ids))


def test_get_transactions_raw():
    yh = yhandler.YHandler('dummy-sc')
    yh.get = MagicMock(return_value=None)
    league_id = "399.l.710921"
    tran_types = "trade"
    count = ""
    expected = "league/{}/transactions;types={};count={}".format(league_id, tran_types, str(count))
    yh.get_transactions_raw(league_id, tran_types, count)
    yh.get.assert_called_with(expected)
    yh.get_transactions_raw(league_id, tran_types, "")
    expected = "league/{}/transactions;types={};count={}".format(league_id, tran_types, "")
    yh.get.assert_called_with(expected)


def test_league_teams_raw():
    yh = yhandler.YHandler('dummy-sc')
    yh.get = MagicMock(return_value=None)
    league_id = "399.l.710921"
    yh.get_league_teams_raw(league_id)
    yh.get.assert_called_with("league/{}/teams".format(league_id))


# Token refresh tests.

def test_is_token_expired_error_401_with_token_expired():
    """Test detection of 401 error with token_expired message."""
    yh = yhandler.YHandler('dummy-sc')

    # Mock response with 401 and token_expired error.
    mock_response = Mock()
    mock_response.status_code = 401
    mock_response.content = b'{"error":{"description":"OAuth oauth_problem=\\"token_expired\\", realm=\\"yahooapis.com\\"}}'

    assert yh._is_token_expired_error(mock_response) is True


def test_is_token_expired_error_403_with_oauth_problem():
    """Test detection of 403 error with oauth_problem message."""
    yh = yhandler.YHandler('dummy-sc')

    # Mock response with 403 and oauth_problem error.
    mock_response = Mock()
    mock_response.status_code = 403
    mock_response.content = b'{"error":{"description":"OAuth oauth_problem=\\"invalid_token\\"}}'

    assert yh._is_token_expired_error(mock_response) is True


def test_is_token_expired_error_200_no_error():
    """Test that 200 responses are not flagged as token expired."""
    yh = yhandler.YHandler('dummy-sc')

    # Mock successful response.
    mock_response = Mock()
    mock_response.status_code = 200
    mock_response.content = b'{"data": "success"}'

    assert yh._is_token_expired_error(mock_response) is False


def test_is_token_expired_error_401_different_error():
    """Test that 401 with non-token errors are not flagged."""
    yh = yhandler.YHandler('dummy-sc')

    # Mock response with 401 but different error.
    mock_response = Mock()
    mock_response.status_code = 401
    mock_response.content = b'{"error":{"description":"Unauthorized access"}}'

    assert yh._is_token_expired_error(mock_response) is False


def test_is_token_expired_error_500_server_error():
    """Test that server errors are not flagged as token expired."""
    yh = yhandler.YHandler('dummy-sc')

    # Mock server error response.
    mock_response = Mock()
    mock_response.status_code = 500
    mock_response.content = b'Internal Server Error'

    assert yh._is_token_expired_error(mock_response) is False


def test_refresh_token_and_retry_success():
    """Test successful token refresh and retry."""
    # Mock OAuth client.
    mock_sc = Mock()
    mock_sc.refresh_access_token = Mock(return_value={
        'access_token': 'new_token_123',
        'token_type': 'bearer',
        'refresh_token': 'refresh_token_456'
    })
    mock_sc.access_token = 'old_token'

    # Create a new session mock that will be returned after refresh.
    mock_new_session = Mock()
    mock_response = Mock()
    mock_response.status_code = 200
    mock_new_session.get = Mock(return_value=mock_response)

    mock_sc.oauth = Mock()
    mock_sc.oauth.get_session = Mock(return_value=mock_new_session)
    mock_sc.session = Mock()

    yh = yhandler.YHandler(mock_sc)

    # Call refresh and retry with method name 'get'.
    result = yh._refresh_token_and_retry('get', 'http://example.com')

    # Verify refresh was called.
    mock_sc.refresh_access_token.assert_called_once()

    # Verify session was updated.
    mock_sc.oauth.get_session.assert_called_once_with(token='new_token_123')

    # Verify method was retried on the NEW session.
    mock_new_session.get.assert_called_once_with('http://example.com')

    # Verify result.
    assert result == mock_response


def test_refresh_token_and_retry_no_refresh_method():
    """Test error handling when refresh_access_token is not available."""
    # Mock OAuth client without refresh method.
    mock_sc = Mock(spec=[])

    yh = yhandler.YHandler(mock_sc)

    # Mock HTTP method.
    mock_method = Mock()

    # Call refresh and retry - should raise RuntimeError.
    try:
        yh._refresh_token_and_retry(mock_method, 'http://example.com')
        assert False, "Should have raised RuntimeError"
    except RuntimeError as e:
        assert b"Token expired and refresh not available" == e.args[0]


def test_get_with_token_refresh():
    """Test that get() automatically refreshes token on expiration."""
    # Mock OAuth client.
    mock_sc = Mock()
    mock_sc.refresh_access_token = Mock(return_value={
        'access_token': 'new_token_123',
        'token_type': 'bearer',
        'refresh_token': 'refresh_token_456'
    })

    # First response: token expired.
    mock_expired_response = Mock()
    mock_expired_response.status_code = 401
    mock_expired_response.content = b'{"error":{"description":"OAuth oauth_problem=\\"token_expired\\"}}'

    # Second response: success after refresh.
    mock_success_response = Mock()
    mock_success_response.status_code = 200
    mock_success_response.json = Mock(return_value={'data': 'success'})

    # Initial session that returns expired response.
    mock_initial_session = Mock()
    mock_initial_session.get = Mock(return_value=mock_expired_response)
    mock_sc.session = mock_initial_session

    # New session after refresh that returns success.
    mock_new_session = Mock()
    mock_new_session.get = Mock(return_value=mock_success_response)

    mock_sc.oauth = Mock()
    mock_sc.oauth.get_session = Mock(return_value=mock_new_session)

    yh = yhandler.YHandler(mock_sc)

    # Make the GET request.
    result = yh.get('test/endpoint')

    # Verify token refresh was called.
    mock_sc.refresh_access_token.assert_called_once()

    # Verify initial session.get was called once.
    assert mock_initial_session.get.call_count == 1

    # Verify new session.get was called once (after refresh).
    assert mock_new_session.get.call_count == 1

    # Verify result.
    assert result == {'data': 'success'}


def test_put_with_token_refresh():
    """Test that put() automatically refreshes token on expiration."""
    # Mock OAuth client.
    mock_sc = Mock()
    mock_sc.refresh_access_token = Mock(return_value={
        'access_token': 'new_token_123',
        'token_type': 'bearer',
        'refresh_token': 'refresh_token_456'
    })

    # First response: token expired.
    mock_expired_response = Mock()
    mock_expired_response.status_code = 401
    mock_expired_response.content = b'{"error":{"description":"OAuth oauth_problem=\\"token_expired\\"}}'

    # Second response: success after refresh.
    mock_success_response = Mock()
    mock_success_response.status_code = 200

    # Initial session that returns expired response.
    mock_initial_session = Mock()
    mock_initial_session.put = Mock(return_value=mock_expired_response)
    mock_sc.session = mock_initial_session

    # New session after refresh that returns success.
    mock_new_session = Mock()
    mock_new_session.put = Mock(return_value=mock_success_response)

    mock_sc.oauth = Mock()
    mock_sc.oauth.get_session = Mock(return_value=mock_new_session)

    yh = yhandler.YHandler(mock_sc)

    # Make the PUT request.
    result = yh.put('test/endpoint', '<xml>data</xml>')

    # Verify token refresh was called.
    mock_sc.refresh_access_token.assert_called_once()

    # Verify initial session.put was called once.
    assert mock_initial_session.put.call_count == 1

    # Verify new session.put was called once (after refresh).
    assert mock_new_session.put.call_count == 1

    # Verify result.
    assert result == mock_success_response


def test_post_with_token_refresh():
    """Test that post() automatically refreshes token on expiration."""
    # Mock OAuth client.
    mock_sc = Mock()
    mock_sc.refresh_access_token = Mock(return_value={
        'access_token': 'new_token_123',
        'token_type': 'bearer',
        'refresh_token': 'refresh_token_456'
    })

    # First response: token expired.
    mock_expired_response = Mock()
    mock_expired_response.status_code = 401
    mock_expired_response.content = b'{"error":{"description":"OAuth oauth_problem=\\"token_expired\\"}}'

    # Second response: success after refresh.
    mock_success_response = Mock()
    mock_success_response.status_code = 201

    # Initial session that returns expired response.
    mock_initial_session = Mock()
    mock_initial_session.post = Mock(return_value=mock_expired_response)
    mock_sc.session = mock_initial_session

    # New session after refresh that returns success.
    mock_new_session = Mock()
    mock_new_session.post = Mock(return_value=mock_success_response)

    mock_sc.oauth = Mock()
    mock_sc.oauth.get_session = Mock(return_value=mock_new_session)

    yh = yhandler.YHandler(mock_sc)

    # Make the POST request.
    result = yh.post('test/endpoint', '<xml>data</xml>')

    # Verify token refresh was called.
    mock_sc.refresh_access_token.assert_called_once()

    # Verify initial session.post was called once.
    assert mock_initial_session.post.call_count == 1

    # Verify new session.post was called once (after refresh).
    assert mock_new_session.post.call_count == 1

    # Verify result.
    assert result == mock_success_response
