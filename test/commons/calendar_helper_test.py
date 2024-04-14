from datetime import datetime

from server.commons.helper.calendar_helper import CalendarHelper


def test_find_current_week_monday():
    date = datetime.strptime("2021-10-06", "%Y-%m-%d")
    monday = CalendarHelper.get_current_week_monday(date)

    assert monday.strftime("%Y-%m-%d") == "2021-10-04"


def test_find_current_week_sunday():
    date = datetime.strptime("2021-10-06", "%Y-%m-%d")
    monday = CalendarHelper.get_current_week_sunday(date)

    assert monday.strftime("%Y-%m-%d") == "2021-10-10"
