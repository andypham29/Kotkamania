from infra.spi.nhlapi.club_stats import ClubStats


def test_get_club_stats_maps_nhl_response(mocker):
    response = mocker.Mock()
    response.json.return_value = {
        'season': '20252026',
        'gameType': 2,
        'skaters': [{
            'playerId': 8479318,
            'headshot': 'https://example.com/matthews.png',
            'firstName': {'default': 'Auston'},
            'lastName': {'default': 'Matthews'},
            'positionCode': 'C',
            'gamesPlayed': 60,
            'goals': 27,
            'assists': 26,
            'points': 53,
            'plusMinus': -4,
            'penaltyMinutes': 18,
            'powerPlayGoals': 5,
            'shorthandedGoals': 0,
            'gameWinningGoals': 3,
            'overtimeGoals': 1,
            'shots': 227,
            'shootingPctg': 0.118943,
            'avgTimeOnIcePerGame': 1248.2333,
            'avgShiftsPerGame': 24.0167,
            'faceoffWinPctg': 0.596708,
        }],
        'goalies': [{
            'playerId': 8479361,
            'headshot': 'https://example.com/woll.png',
            'firstName': {'default': 'Joseph'},
            'lastName': {'default': 'Woll'},
            'gamesPlayed': 39,
            'gamesStarted': 38,
            'wins': 15,
            'losses': 16,
            'overtimeLosses': 7,
            'goalsAgainstAverage': 3.336221,
            'savePercentage': 0.89918,
            'shotsAgainst': 1220,
            'saves': 1097,
            'goalsAgainst': 124,
            'shutouts': 2,
            'goals': 0,
            'assists': 1,
            'points': 1,
            'penaltyMinutes': 2,
            'timeOnIce': 133804,
        }],
    }
    get = mocker.patch('infra.spi.nhlapi.club_stats.requests.get', return_value=response)

    stats = ClubStats().get_club_stats('tor', '20252026')

    get.assert_called_once_with(
        'https://api-web.nhle.com/v1/club-stats/TOR/20252026/2',
        timeout=10,
    )
    response.raise_for_status.assert_called_once_with()
    assert stats.season == '20252026'
    assert stats.skaters[0].first_name.default == 'Auston'
    assert stats.skaters[0].shooting_percentage == 0.118943
    assert stats.goalies[0].last_name.default == 'Woll'
    assert stats.goalies[0].save_percentage == 0.89918
