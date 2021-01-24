class FantasyGoalieGradeHelper:

    def __init__(self):
        pass

    def getGoalieGrade(self, skaterFullName, player_stat):
        grade = 0
        if player_stat is None:
            return 0

        grade_wins = self.__calculate_grade_wins(player_stat)
        grade_save_avg = self.__calculate_grade_save_percentage(player_stat)
        grade_save_even = self.__calculate_grade_save_percentage_even(player_stat)
        grade_save_pp = self.__calculate_grade_save_percentage_pp(player_stat)
        grade_save_pk = self.__calculate_grade_save_percentage_pk(player_stat)
        index_shutouts = self.__calculate_index_shutout(player_stat)

        scale = self.__scale_by_games_played(player_stat)

        grade += (1.75 + index_shutouts * 0.25) * (
                    grade_wins * 3 + grade_save_even * 2.5 + grade_save_pp + grade_save_pk + grade_save_avg * 2.5) / 2
        grade = grade * scale
        print(skaterFullName, grade, grade_wins + grade_save_even + grade_save_pp + grade_save_pk + grade_save_avg)
        return round(grade, 2)

    def __scale_by_games_played(self, player_stat):
        gp = player_stat.games
        gp = gp if gp else 1
        if gp < 10:
            return 0.6
        elif 10 <= gp < 20:
            return 0.9
        elif 20 <= gp < 30:
            return 0.95
        else:
            return 1

    def __calculate_grade_games_played(self, player_stat):
        games = player_stat.games

    def __calculate_grade_wins(self, player_stat):
        # return -0.003 * (player_stat.goals / player_stat.games * 82 - 70) ** 2 + 10
        wins = player_stat.wins / player_stat.games * 100
        win_percent = wins if wins else 0

        if win_percent < 49:
            return 7
        elif 49 <= win_percent < 51:
            return 7.5
        elif 51 <= win_percent < 53:
            return 7.8
        elif 53 <= win_percent < 55:
            return 8
        elif 55 <= win_percent < 57:
            return 8.5
        elif 57 <= win_percent < 60:
            return 8.8
        elif 60 <= win_percent < 63:
            return 9
        elif 63 <= win_percent < 66:
            return 9.5
        elif 66 <= win_percent < 70:
            return 10
        else:
            return 10.5

    def __calculate_grade_goals_against(self, player_stat):
        # return -0.0015 * (player_stat.assists / player_stat.games * 82 - 100) ** 2 + 10
        goal_against = player_stat.goalAgainstAverage
        goal_against = goal_against if goal_against is not None else 10

        if goal_against > 5:
            return 5
        elif 5 >= goal_against > 4:
            return 6
        elif 4 >= goal_against > 3:
            return 7
        elif 3 >= goal_against > 2.5:
            return 8
        elif 2.5 >= goal_against > 2:
            return 9
        elif 2 >= goal_against > 1.5:
            return 9.5
        elif 1.5 >= goal_against > 1:
            return 10
        else:
            return 10.5

    def __calculate_grade_save_percentage(self, player_stat):
        # return -0.0007 * (player_stat.points / player_stat.games * 82 - 150) ** 2 + 10
        percent = player_stat.savePercentage
        percent = percent * 100 if percent is not None else 0

        if percent < 84:
            return 6
        elif 84 <= percent < 88:
            return 6.5
        elif 88 <= percent < 89:
            return 7
        elif 89 <= percent < 90:
            return 7.5
        elif 90 <= percent < 90.5:
            return 7.8
        elif 90.5 <= percent < 91:
            return 8
        elif 91 <= percent < 91.5:
            return 8.5
        elif 91.5 <= percent < 92:
            return 8.8
        elif 92 <= percent < 92.5:
            return 9
        elif 92.5 <= percent < 93:
            return 9.3
        elif 93 <= percent < 95:
            return 9.5
        else:
            return 10

    def __calculate_grade_save_percentage_pp(self, player_stat):
        # return -0.0007 * (player_stat.percent / player_stat.games * 82 - 100) ** 2 + 10
        percent = player_stat.powerPlaySavePercentage
        percent = percent if percent is not None else 0

        if percent < 84:
            return 6
        elif 84 <= percent < 86:
            return 7.5
        elif 86 <= percent < 88:
            return 8
        elif 88 <= percent < 90:
            return 8.5
        elif 90 <= percent < 91:
            return 8.8
        elif 92 <= percent < 93:
            return 9
        elif 93 <= percent < 95:
            return 9.5
        else:
            return 10

    def __calculate_grade_save_percentage_pk(self, player_stat):
        # return player_stat.powerPlayGoals / player_stat.games * 8
        percent = player_stat.shortHandedSavePercentage
        percent = percent if percent is not None else 0

        if percent < 84:
            return 6
        elif 84 <= percent < 86:
            return 7
        elif 86 <= percent < 88:
            return 7.5
        elif 88 <= percent < 90:
            return 8.8
        elif 90 <= percent < 91:
            return 9.3
        elif 92 <= percent < 93:
            return 9.5
        elif 93 <= percent < 95:
            return 9.8
        else:
            return 10

    def __calculate_grade_save_percentage_even(self, player_stat):
        # return player_stat.powerPlayPoints / player_stat.games * 10
        percent = player_stat.shortHandedSavePercentage
        percent = percent if percent is not None else 0
        if percent < 84:
            return 6
        elif 84 <= percent < 86:
            return 6.5
        elif 86 <= percent < 88:
            return 7
        elif 88 <= percent < 90:
            return 7.5
        elif 90 <= percent < 91:
            return 8
        elif 92 <= percent < 93:
            return 8.5
        elif 93 <= percent < 95:
            return 9
        elif 95 <= percent < 97:
            return 9.5
        else:
            return 10

    def __calculate_index_shutout(self, player_stat):
        # return player_stat.powerPlayPoints / player_stat.games * 10
        index = player_stat.shutouts

        if index < 2 or index is None:
            return 1
        elif 2 <= index < 3:
            return 1.01
        elif 3 <= index < 5:
            return 1.02
        elif 5 <= index < 7:
            return 1.03
        elif 7 <= index < 9:
            return 1.04
        else:
            return 1.05
