from datetime import datetime


class TimeConverter:

    @staticmethod
    def convert_string_to_total_seconds(time):
        time = datetime.strptime(time, '%M:%S')
        return time.minute * 60 + time.second
