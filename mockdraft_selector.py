# test value
import random, schedule

from model.prospect import ProspectElite
from model.draftpick import DraftPick
from repository.prospect_elite_dao import ProspectEliteDao
from helper.http_helper import HttpHelper

# from nhl import allDivision
class MockDraftSelector:
    def __init__(self, prospectlist):
        self.prospectlist = self.__getSortedListByAvgRank(prospectlist)

    def __getPlayerPoints(self,prospect):
        # 5*(32 - rank_site1) + 5*(32 - rank_site2) + ...
        points = 0
        list = [prospect.hp, prospect.fc, prospect.iss, prospect.mh, prospect.elite]
        for item in list:
            if str.isdigit(item):
                if int(item) < 32:
                    points += 10
                points += (32 - int(item))*100
            else:
                points += 100

        # print("points: ", points)
        return points

    def __getPlayerBestPoints(self, prospect):
        # 5*(32 - rank_site1) + 5*(32 - rank_site2) + ...
        points = (32 - self.__getPlayerBestRank(prospect))*100*5
        if points < 0:
            return 500
        return points

    def __getPlayerWorstPoints(self, prospect):
        # 5*(32 - rank_site1) + 5*(32 - rank_site2) + ...
        points = (32 - self.__getPlayerWorstRank(prospect))*100*5
        if points < 0:
            return 0
        return points

    def __getPlayerAvgRank(self, prospect):
        total = 0
        count = 0
        list = [prospect.hp, prospect.fc, prospect.iss, prospect.mh, prospect.elite]
        if list[0:4] == "-":
            total = 45*5
        for item in list:
            if str.isdigit(item):
                count += 1
                total += int(item)
            else:
                count += 1
                total += 42
        # print("avg_rank: ", total/count)
        return total/count

    def __getPlayerRangeRank(self, prospect):
        val_list = [prospect.hp, prospect.fc, prospect.iss, prospect.mh, prospect.elite]
        if "-" in val_list:
            for item in range(val_list.count("-")):
                val_list.remove("-")

        if len(val_list) == 0:
            return 40

        min_val = min(val_list)
        max_val = max(val_list)


        return int(max_val) - int(min_val)

    def __getPlayerBestRank(self, prospect):
        val_list = [prospect.hp, prospect.fc, prospect.iss, prospect.mh, prospect.elite]
        if "-" in val_list:
            for item in range(val_list.count("-")):
                val_list.remove("-")
        if len(val_list) == 0:
            return 45

        return int(min(val_list))

    def __getPlayerWorstRank(self, prospect):
        val_list = [prospect.hp, prospect.fc, prospect.iss, prospect.mh, prospect.elite]
        if "-" in val_list:
            for item in range(val_list.count("-")):
                val_list.remove("-")
        if len(val_list) == 0:
            return 45

        return int(max(val_list))

    def __getPlayerMeanRank(self, prospect):
        total = 0
        count = 0
        list = [prospect.hp, prospect.fc, prospect.iss, prospect.mh, prospect.elite]
        for item in list:
            if str.isdigit(item):
                count += 1
                total += int(item)
            else:
                count += 1
                total += 45
        return total/count

    def __getPlayerBalls(self, prospect, current_pick):
        # points/10^((weighted_rank/110)/current_pick)
        avg_rank = self.__getPlayerAvgRank(prospect)
        points = self.__getPlayerPoints(prospect)
        best_points = self.__getPlayerBestPoints(prospect)
        worst_points = self.__getPlayerWorstPoints(prospect)
        range = self.__getPlayerRangeRank(prospect)
        best_rank = self.__getPlayerBestRank(prospect)
        worst_rank = self.__getPlayerWorstRank(prospect)

        # denominator to determine
        options = {
                0 : 10**((25*avg_rank + 65*best_rank + 10*worst_rank)/100/(current_pick)),
                1 : 10**((30*avg_rank + 30*best_rank + 40*worst_rank)/100/(current_pick)),
                2 : 10**(avg_rank/current_pick),
                3 : 10**(worst_rank/current_pick),
               }

        # factor to determin if player raise, drop or same odds
        factor = 20*(current_pick/(0.7*avg_rank + 0.3*worst_rank)) if current_pick > (worst_rank + 2) else 1
        denom = options[1]

        rand = random.randrange(0,19)
        rand2 = 10
        # rand2 = random.randrange(0,19)

        if rand == 2:
            factor *= 1.1
        if rand == 1:
            factor *= 0.9

        if rand2 == 0:
            denom = options[0]
        if rand2 == 1:
            denom = options[3]
        if 1 <= rand2 < 9:
            denom = options[2]



        returned_balls = points/denom * factor
        if avg_rank == 42:
            return 0
        return returned_balls

    def __getRandomBall(self, total_balls):
        if total_balls == 0 or total_balls == 1:
            return 0
        return random.randrange(0, total_balls - 1)

    def __getPlayerRebalancedBall(self, prospect, next_prospect, current_pick):
        player_balls = int(self.__getPlayerBalls(prospect, current_pick))
        next_player_balls = int(self.__getPlayerBalls(next_prospect, current_pick))

        if (player_balls <= 5 and next_player_balls <= 20):
            player_rebalanced_balls = int(self.__getPlayerBalls(prospect, current_pick + 1))
            return player_rebalanced_balls if player_rebalanced_balls > 10 else 0

        return 0

    def __getPickOdds(self, list_ball, picked_ball):
        odds = 0
        total = list_ball[len(list_ball) - 1]

        if total == 0:
            return 100
        for i in range(len(list_ball)):
            if list_ball[i] >= picked_ball:
                if i == 0:
                    odds = list_ball[i]
                    break
                else:
                    odds = list_ball[i] - list_ball[i-1]
                    break

        return odds/total * 100

    def pickPlayerBySelection(self, current_pick):
        if current_pick == 0:
            return
        prospectlist = self.prospectlist
        list = []
        total_balls = 0
        for i in range(len(prospectlist)):
            prospect = prospectlist[i]
            player_balls = int(self.__getPlayerBalls(prospect, current_pick))

            if player_balls > 0:
                total_balls += player_balls
                list.append(total_balls)

            elif i < len(prospectlist) - 1 and player_balls <= 0:
                next_prospect = prospectlist[i+1]
                next_player_balls = int(self.__getPlayerBalls(next_prospect, current_pick))

                player_rebalanced_balls = self.__getPlayerRebalancedBall(prospect, prospectlist[i+1], current_pick)
                if player_rebalanced_balls <= 5 and player_balls != 0:
                    total_balls += player_rebalanced_balls
                    list.append(total_balls)

            else:
                break

        # if total_balls == 0:
        #     list.append(0)
        picked_ball = self.__getRandomBall(total_balls)

        # check list of ball
        for i in range(len(list)):
            if picked_ball <= list[i]:
                print("pick ", current_pick, ": \t", prospectlist[i].name_position, "\t\tavg: ", prospectlist[i].avg_rank, "\thp: ", prospectlist[i].hp, "fc: ", prospectlist[i].fc, "iss: ", prospectlist[i].iss, "mh: ", prospectlist[i].mh, "elite: ", prospectlist[i].elite)
                print("odds: ", self.__getPickOdds(list, picked_ball),"  ",list, "ball: ", picked_ball)
                prospect_picked = DraftPick(pick=current_pick, name_position= prospectlist[i].name_position, odds=self.__getPickOdds(list, picked_ball), list_ball=list, picked_ball=picked_ball)
                prospectlist.pop(i)
                return prospect_picked
                # break


    def __getSortedListByAvgRank(self, list):
        for i in range(len(list)):
            list[i].avg_rank = self.__getPlayerAvgRank(list[i])
        return sorted(list, key=lambda x: x.avg_rank, reverse=False)

url = 'https://statsapi.web.nhl.com/api/v1/standings'
#
def getTeams():
    json = HttpHelper.get(url)
    return allDivision(json['records'])



# prospects = ProspectEliteDao().getAllProspects()

print("-------------------------------------------------------------------------------------------------------------------------------")
# pickPlayer(getSortedListByAvgRank(prospects), 1)

# print(allDivision(getTeams()))
# list = getSortedListByAvgRank(prospects)
# for i in range(len(list)):
#     print(list[i])
