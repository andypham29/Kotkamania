from setting import Setting


class NhlYearConverter:

    @staticmethod
    def get_current_season():
        current_year = int(Setting.NHL_YEAR)
        return f"{current_year - 1}{current_year}"

    @staticmethod
    def get_previous_season_by_year_removed(minus_year):
        current_year = int(Setting.NHL_YEAR)
        return f"{current_year - minus_year - 1}{current_year - minus_year}"
