from datetime import datetime


class TimeConverter:

    @staticmethod
    def convert_string_to_total_seconds(time):
        time = datetime.strptime(time, '%M:%S')
        return time.minute * 60 + time.second

    @staticmethod
    def convert_total_seconds_to_string(seconds):
        s = int(seconds % 60)
        m = str(int((seconds - s) / 60))
        s = f"0{s}" if s < 10 else f"{s}"

        return f"{m}:{s}"
