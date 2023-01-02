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

    def get_gper60_index_for_last_10(self, gamelogs):
        last_five_games = reversed(gamelogs[:10])
        toi = 0
        g = 0
        for game in last_five_games:
            toi = toi + TimeConverter.convert_string_to_total_seconds(game.timeOnIce)
            g = g + game.goals

        g_per_60 = 0 if (g == 0) else g / toi * 60 * 60
        return round(g_per_60, 2)

    def get_ptsper60_index_for_last_10(self, gamelogs):
        last_five_games = reversed(gamelogs[:10])
        toi = 0
        g = 0
        for game in last_five_games:
            toi = toi + TimeConverter.convert_string_to_total_seconds(game.timeOnIce)
            g = g + game.points

        g_per_60 = 0 if (g == 0) else g / toi * 60 * 60
        return round(g_per_60, 2)

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

    def get_peripheral_index_for_last_5(self, sogs_percentiles, hits_percentiles, blocked_percentiles, gamelogs):
        last_five_games = reversed(gamelogs[:5])
        sogs_counter = 0
        hits_counter = 0
        blocked_counter = 0

        for game in last_five_games:
            sogs_counter += self.__peripheral_counter(game, "shots", sogs_percentiles)
            hits_counter += self.__peripheral_counter(game, "hits", hits_percentiles)
            blocked_counter += self.__peripheral_counter(game, "blocked", blocked_percentiles)

        return round(sogs_counter + hits_counter + blocked_counter, 2)

    def __peripheral_counter(self, game, stat_name, stat_percentiles):
        counter = 0
        current_stat = getattr(game, stat_name)
        current_stat = current_stat if current_stat else 0
        if current_stat > stat_percentiles[18]:
            counter += 1.25
        elif current_stat > stat_percentiles[17]:
            counter += 1
        elif current_stat > stat_percentiles[14]:
            counter += 0.75
        elif current_stat > stat_percentiles[9]:
            counter += 0.5
        else:
            counter += 0
        return counter
