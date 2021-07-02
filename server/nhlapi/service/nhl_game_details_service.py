from helper.http_helper import HttpHelper


class NhlGameDetailsService:

    def __init__(self):
        pass

    def getGameIdByDay(self):
        json = HttpHelper.get('https://statsapi.web.nhl.com/api/v1/schedule')
        schedule = json.get('dates')[0].get('games')

        return [game_info.get('gamePk') for game_info in schedule]

    def getGameDetails(self, game_id):
        json = HttpHelper.get(f'https://statsapi.web.nhl.com/api/v1/game/{game_id}/feed/live')
        plays = json.get('liveData').get('plays').get('allPlays')

        return plays

    def getAllEvents(self, game_details):
        events = dict()
        for item in game_details:
            event_type_id = item.get('result').get('eventTypeId')

            if event_type_id in events.keys():
                events[event_type_id] += 1
            else:
                events[event_type_id] = 1

        return events

    def getAllByEvent(self, event, game_details):
        events = []

        for item in game_details:
            if item.get('result').get('eventTypeId') == event:
                events.append(item)

        return events

    def getAllByTeamCode(self, team_code, game_details):
        events = []

        for item in game_details:
            team = item.get('team')
            if team is None:
                continue
            if team.get('triCode') == team_code:
                events.append(item)

        return events

    def getAllByPeriod(self, period, game_details):
        events = []

        for item in game_details:
            if item.get('about').get('period') == period:
                events.append(item)

        return events

    def getAllByPlayer(self, player_name, game_details):
        events = []

        for item in game_details:
            players = item.get('players', [])

            if player_name in [p.get('player').get('fullName') for p in players if p is not None]:
                events.append(item)

        return events


class TestScript:

    def __init__(self, game_details):
        self.game_details = game_details

    def printAllEvents(self):
        # for i in NhlGameDetailsService().getAllEvents(self.game_details):
        print(NhlGameDetailsService().getAllEvents(self.game_details))

    def printAllEventIds(self):
        event_ids = NhlGameDetailsService().getAllEvents(self.game_details)

        for i in event_ids:
            print(i)

    def printAllByEventId(self, event_id):
        events = NhlGameDetailsService().getAllByEvent(event_id, self.game_details)
        print(f'{event_id}: {len(events)}')
        for i in events:
            print(i)

    def printAllByTeamCode(self, team_code):
        for i in NhlGameDetailsService().getAllByTeamCode(team_code, self.game_details):
            print(i)

    def printAllByPlayer(self, player_name):
        for i in NhlGameDetailsService().getAllByPlayer(player_name, self.game_details):
            print(i)


if __name__ == '__main__':
    # print(NhlGameDetailsService().getGameIdByDay())
    # game_details = NhlGameDetailsService().getGameDetails('2020020709')
    # game_details = NhlGameDetailsService().getGameDetails('2020020546')
    # game_details = NhlGameDetailsService().getGameDetails('2020020645')
    game_details = NhlGameDetailsService().getGameDetails('2020030411')

    # for i in game_details:
    #     print(i)
    mtl_game_details = NhlGameDetailsService().getAllByTeamCode('MTL', game_details)
    mtl_game_details_period3 = NhlGameDetailsService().getAllByPeriod(3, mtl_game_details)

    tbl_game_details = NhlGameDetailsService().getAllByTeamCode('TBL', game_details)

    a = TestScript(mtl_game_details)
    b = TestScript(tbl_game_details)
    event_ids = NhlGameDetailsService().getAllEvents(mtl_game_details)

    a.printAllEvents()
    b.printAllEvents()
    # a.printAllByPlayer('Jonathan Drouin')
    # a.printAllByEventId('GOAL')
    # a.printAllByEventId('GIVEAWAY')
    # b.printAllByEventId('MISSED_SHOT')
    # a.printAllByTeamCode('MTL')
