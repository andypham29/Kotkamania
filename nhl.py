#!/usr/bin/env python3

from model.team import Team, Player
from model.prospect import Prospect
from repository.prospect_dao import ProspectDao
from http_helper import HttpHelper

import calendar, datetime
import json
import sys, schedule, time
import random

url = 'https://statsapi.web.nhl.com/api/v1/standings'
urlPlayer = 'https://api.nhle.com/stats/rest/en/skater/summary?isAggregate=false&isGame=false&sort=%5B%7B%22property%22:%22points%22,%22direction%22:%22DESC%22%7D%5D&start=0&limit=100&factCayenneExp=gamesPlayed%3E=1&cayenneExp=gameTypeId=2%20and%20seasonId%3C=20192020%20and%20seasonId%3E=20192020'
baseUrlPlayer = 'https://statsapi.web.nhl.com/api/v1/people/'

helpMessage = """
Usage: python nhl.py  [options...]

-p, --player\t Get Player statistics by rank <rank>
-P, --playerId\t Get Player statistics by Id <id> and season <season>
-t, --teams\t Get NHL team standings
-s, --schedule\t Test python schduler: Get Player statistic randomly every 1 second
-w, --webScrape\t Scrape Website
-a, --append\t Append to target file when uploading"""

# api methods
def allDivision(json):
    for item in json:
        allTeamPerDivision(item['teamRecords'])

def allTeamPerDivision(json):
    for item in json:
        name = item['team']['name']
        record = item['leagueRecord']
        leagueRank = item['leagueRank']

        # print("({0}) {1}: {2}".format(leagueRank, name, record))
        team = Team(name, record, leagueRank)
        team.toString()

# script methods
def job():
    player = getPlayerByRank(random.randint(0,49))
    value = json.dumps(player.__dict__)
    print(value)

def getPlayerByRank(index):
    json = json = HttpHelper.get(urlPlayer)['data'][index]

    rank = index + 1
    playerId = json['playerId']
    fullName = json['skaterFullName']
    position = json['positionCode']
    team = json['teamAbbrevs']
    gamesPlayed = json['gamesPlayed']
    goals = json['goals']
    assists = json['assists']
    points = json['points']

    return Player(rank, playerId, fullName, position, team, gamesPlayed, goals, assists, points)

def getPlayerById(id, season):
    playerJson = HttpHelper.get(baseUrlPlayer + str(id))
    seasonJson = HttpHelper.get(baseUrlPlayer + str(id) + "/stats?stats=statsSingleSeason&season=" + season)

    playerId = playerJson['people'][0]['id']
    fullName = playerJson['people'][0]['fullName']
    position = playerJson['people'][0]['primaryPosition']['abbreviation']
    team = playerJson['people'][0]['currentTeam']['name']
    gamesPlayed = seasonJson['stats'][0]['splits'][0]['stat']['games']
    goals = seasonJson['stats'][0]['splits'][0]['stat']['goals']
    assists = seasonJson['stats'][0]['splits'][0]['stat']['assists']
    points = seasonJson['stats'][0]['splits'][0]['stat']['points']

    return Player("", playerId, fullName, position, team, gamesPlayed, goals, assists, points)

if(len(sys.argv) == 1 or sys.argv[1] in ["--help", "-h"]):
    print(helpMessage)

elif(sys.argv[1] in ["--player", "-p"]):
    index = int(sys.argv[2])

    player = getPlayerByRank(index)
    print(json.dumps(player.__dict__))

elif(sys.argv[1] in ["--playerId", "-P"]):
    id = int(sys.argv[2])
    season = sys.argv[3]

    player = getPlayerById(id, season)
    print(json.dumps(player.__dict__))

elif(sys.argv[1] in ["--teams", "-t"]):
    json = HttpHelper.get(url)
    allDivision(json['records'])

elif(sys.argv[1] in ["--schedule", "-s"]):
    schedule.every(1).seconds.do(job)
    while 1:
        schedule.run_pending()
        time.sleep(1)
    # schedule.every(10).minutes.do(job)
    # schedule.every().hour.do(job)
    # schedule.every().day.at("10:30").do(job)

elif(sys.argv[1] in ["--webScrape", "-w"]):
    if len(sys.argv) >= 3 :
        id = int(sys.argv[2])
        # ProspectDao().initProspectTable()
        # ProspectDao().createProspect(p)
        prospect = ProspectDao().getProspectById(id)
        print(json.dumps(prospect.__dict__))
    else:
        prospects = ProspectDao().getAllProspects()
        print(json.dumps([prospect.__dict__ for prospect in prospects]))

# cal = calendar.TextCalendar(calendar.SUNDAY)
# d = datetime.datetime.today()
#
#
# print("Date: %s/%s/%s\n" % (d.month, d.day, d.year))
# print(cal.formatmonth(d.year, d.month, 1))
