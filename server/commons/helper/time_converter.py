from datetime import datetime


class TimeConverter:

    @staticmethod
    def convert_string_to_total_seconds(time):
        if time is None:
            return 0
        time = datetime.strptime(time, '%M:%S')
        return time.minute * 60 + time.second

    @staticmethod
    def convert_total_seconds_to_string(seconds):
        s = int(seconds % 60)
        m = int((seconds - s) / 60)
        s = f"0{s}" if s < 10 else f"{s}"
        m = f"0{m}" if m < 10 else f"{m}"

        return f"{m}:{s}"
