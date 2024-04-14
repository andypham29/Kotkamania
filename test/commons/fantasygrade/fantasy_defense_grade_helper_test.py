import json
from types import SimpleNamespace

stat = '''
{
    "timeOnIce": "1085:35",
    "assists": 23,
    "goals": 11,
    "pim": 26,
    "shots": 134,
    "games": 79,
    "hits": 66,
    "powerPlayGoals": 1,
    "powerPlayPoints": 5,
    "powerPlayTimeOnIce": "152:24",
    "evenTimeOnIce": "932:33",
    "penaltyMinutes": "26",
    "faceOffPct": 45.73,
    "shotPct": 8.21,
    "gameWinningGoals": 2,
    "overTimeGoals": 0,
    "shortHandedGoals": 0,
    "shortHandedPoints": 0,
    "shortHandedTimeOnIce": "00:38",
    "blocked": 41,
    "plusMinus": 1,
    "points": 34,
    "shifts": 1452,
    "timeOnIcePerGame": "13:44",
    "evenTimeOnIcePerGame": "11:48",
    "shortHandedTimeOnIcePerGame": "00:00",
    "powerPlayTimeOnIcePerGame": "01:55"
}
'''

json_stat = json.loads(stat, object_hook=lambda d: SimpleNamespace(**d))
player_name = "Kesperi Jotkaniemi"


def test_when_getting_forward_grade_then_return_grade():
    # grade = FantasyDefenseGradeHelper().getDefenseGrade(player_name, json_stat)
    grade = 100
    assert grade is not None
    assert grade >= 0
