from datetime import timedelta, datetime


class CalendarHelper:

    @staticmethod
    def get_current_day():
        return datetime.now().date()

    @staticmethod
    def get_current_week_monday(today=datetime.now().date()):
        monday = today - timedelta(days=today.weekday())
        return monday

    @staticmethod
    def get_current_week_sunday(today=datetime.now().date()):
        sunday = today - timedelta(days=today.weekday() - 6)
        return sunday


if __name__ == '__main__':
    print(CalendarHelper.get_current_week_monday().day)
    print(CalendarHelper.get_current_day().day)
    print(CalendarHelper.get_current_week_sunday().day)
