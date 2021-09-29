import json
from types import SimpleNamespace

from server.commons.fantasygrade.fantasy_forward_grade_helper import FantasyForwardGradeHelper
from server.commons.fantasygrade.fantasy_player_grader import FantasyPlayerGrader, Grade
from server.nhlapi.service.nhl_player_stat_service import NHLPlayerStatService

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

stat2 = '''
{
    "timeOnIce": "139:36",
    "assists": 1,
    "goals": 4,
    "pim": 2,
    "shots": 30,
    "games": 10,
    "hits": 3,
    "powerPlayGoals": 0,
    "powerPlayPoints": 0,
    "powerPlayTimeOnIce": "15:58",
    "evenTimeOnIce": "123:38",
    "penaltyMinutes": "2",
    "faceOffPct": 0,
    "shotPct": 13.3,
    "gameWinningGoals": 2,
    "overTimeGoals": 2,
    "shortHandedGoals": 0,
    "shortHandedPoints": 0,
    "shortHandedTimeOnIce": "00:00",
    "blocked": 0,
    "plusMinus": -1,
    "points": 5,
    "shifts": 191,
    "timeOnIcePerGame": "13:57",
    "evenTimeOnIcePerGame": "12:21",
    "shortHandedTimeOnIcePerGame": "00:00",
    "powerPlayTimeOnIcePerGame": "01:35"
}
'''
json_stat = json.loads(stat2, object_hook=lambda d: SimpleNamespace(**d))
player_name = "Jesperi Kotkaniemi"


def test_when_getting_forward_grade_then_return_grade():
    grade = FantasyForwardGradeHelper().getForwardGrade(player_name, json_stat)
    assert grade is not None
    assert grade >= 0


def test_when_getting_forward_under25_grade_then_return_grade():
    grade = FantasyForwardGradeHelper().getForwardGrade(player_name, json_stat)
    assert grade is not None
    print(player_name, ": ", grade)
    assert grade >= 30


def test2():
    grade = Grade(
        FantasyForwardGradeHelper().getForwardGrade(player_name, json_stat),
        0,
        0,
        0
    )
    player_final_grade = FantasyPlayerGrader.calculate_overall_grade("Cole Caufield", grade)
    print(player_final_grade)
    assert player_final_grade >= 30


def test():
    playoff_stat = NHLPlayerStatService().get_player_playoff_stat_by_playerId_and_seasons("8481540", ["20202021"])
    grade_20202021_p = FantasyForwardGradeHelper().getForwardGrade(player_name, playoff_stat[0].stat)
    grade_20202021 = FantasyForwardGradeHelper().getForwardGrade(player_name, json_stat)
    grade_20192020 = 0
    grade_20182019 = 0
    grade_20172018 = 0

    if grade_20202021_p > 0:
        grade = (
                            grade_20202021_p * 4 + grade_20202021 * 7 + grade_20192020 * 8 + grade_20182019 * 5 + grade_20172018 * 1) / 25
    else:
        grade = (grade_20202021 * 7 + grade_20192020 * 12 + grade_20182019 * 5 + grade_20172018 * 1) / 25
    grade = round(grade, 2)

    assert grade is not None
    print(player_name, ": ", grade)
    assert grade >= 30
