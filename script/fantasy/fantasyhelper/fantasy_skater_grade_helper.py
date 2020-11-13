import datetime


class FantasySkaterGradeHelper:

    def __init__(self):
        pass

    def getSkaterGrade(self, player):
        grade = 0

        for player_stat in player.stats:
            toi = datetime.datetime.strptime(player_stat.stat.timeOnIcePerGame, '%M:%S')
            pptoi = datetime.datetime.strptime(player_stat.stat.powerPlayTimeOnIcePerGame, '%M:%S')
            evtoi = datetime.datetime.strptime(player_stat.stat.evenTimeOnIcePerGame, '%M:%S')

            grade1 = (-0.003 * (player_stat.stat.goals / player_stat.stat.games * 82 - 60) ** 2 + 10)
            grade2 = (-0.0015 * (player_stat.stat.assists / player_stat.stat.games * 82 - 80) ** 2 + 10)
            grade3 = (-0.0007 * (player_stat.stat.points / player_stat.stat.games * 82 - 120) ** 2 + 10)
            grade4 = player_stat.stat.powerPlayGoals / player_stat.stat.games * 8
            grade5 = (player_stat.stat.powerPlayPoints - player_stat.stat.powerPlayGoals) / player_stat.stat.games * 6
            grade6 = player_stat.stat.powerPlayPoints / player_stat.stat.games * 10
            grade7 = (player_stat.stat.shotPct / 100) ** -1 * 0.1
            grade8 = (toi.minute * 60 + toi.second) / (20 * 60)
            grade9 = (pptoi.minute * 60 + pptoi.second) / (3 * 60)
            grade10 = (evtoi.minute * 60 + evtoi.second) / (15 * 60)

            shoot = self.shotPctIndex(player_stat.stat.shotPct)
            general = ((grade4 * shoot + grade5 + grade6 + grade7) + ((grade8 + grade9 + grade10) * shoot / 3) * 0.8)

            print(
                f"{player.fullName}[{round(shoot, 2)}]: \t\tGEN:{round(general, 2)}\tPP:{round(grade8, 2)}\tEV:{round(grade10, 2)} {player_stat.stat.assists / player_stat.stat.games * 82}\t{grade3} {player_stat.stat.points / player_stat.stat.games * 82}")
            grade += (grade1 * shoot + grade2 + grade3 + general) / 42 * 100

        return round(grade, 2)

    def shotPctIndex(self, shotPct):
        return round(-0.055 * (shotPct / 12) ** 3 + 1.05, 2)
