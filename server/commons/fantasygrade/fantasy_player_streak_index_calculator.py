from server.commons.helper.time_converter import TimeConverter


class FantasyPlayerStreakIndexCalculator:

    def __init__(self):
        pass

    def get_point_index_for_last_5(self, gamelogs):
        last_five_games = gamelogs[:5]
        counter = 0
        no_point_streak = 0
        for i in range(len(last_five_games)):
            point = last_five_games[i].points
            if point > 0:
                no_point_streak = 0
                counter += 1 + 0.25 * (point - 1)
            else:
                no_point_streak += 1
                counter -= 0.1 * no_point_streak
        return round(counter, 2)

    def get_toi_index_for_last_5(self, gamelogs):
        last_five_games = reversed(gamelogs[:5])
        counter = 0
        last_toi = 0
        for game in last_five_games:
            toi = TimeConverter.convert_string_to_total_seconds(game.timeOnIce)
            if 0 < last_toi < toi:
                counter += 1
                counter += (toi - last_toi) / toi
            if toi > 15 * 60:
                counter += 0.5
            last_toi = toi
        return round(counter, 2)

    def get_pptoi_index_for_last_5(self, gamelogs):
        last_five_games = reversed(gamelogs[:5])
        counter = 0
        last_pptoi = 0
        for game in last_five_games:
            pptoi = TimeConverter.convert_string_to_total_seconds(game.powerPlayTimeOnIce)
            if 0 < last_pptoi < pptoi and pptoi > 30:
                counter += 1
                counter += (pptoi - last_pptoi) / pptoi
            if pptoi > 1 * 60:
                counter += 0.25
            if pptoi > 2 * 60:
                counter += 0.25
            last_pptoi = pptoi
        return round(counter, 2)
