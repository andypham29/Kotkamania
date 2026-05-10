import json

from flask import Flask, request, render_template, make_response

from domain.gamelog.service.gamelog_service import GameLogService
from server.admin.service.facade.admin_facade import AdminFacade
from server.internaldata.service.facade.fantasy_nhl_player_facade import FantasyNhlPlayerFacade
from server.internaldata.service.fantasy_nhl_player_service import FantasyNhlPlayerService
from server.internaldata.service.fantasy_player_streak_index_service import FantasyPlayerStreakIndexService
from server.mockdraft.service.facade.mockdraft_selector_service_facade import MockDraftSelectorServiceFacade
from server.mockdraft.service.prospect_elite_service import ProspectEliteService
from server.nhlapi.service.facade.nhl_player_service_facade import NHLPlayerServiceFacade
from server.nhlapi.service.facade.nhl_roster_service_facade import NHLRosterServiceFacade
from server.nhlapi.service.nhl_schedule_service import NHLScheduleService
from server.nhlapi.service.nhl_stats_leader_service import NHLStatsLeaderService
from server.nhlapi.service.nhl_team_service import NhlTeamService
from server.twitterapi.service.facade.twitter_service_facade import TwitterServiceFacade
from setting import Setting

app = Flask(__name__)


# Admin Routing
@app.route('/admin/script/<offset>')
def runSystemScript(offset):
    api_key = request.headers.get('x-api-key')
    if api_key != Setting.KKMANIA_API_KEY:
        return make_response("Unable to access resource.", 401)
    response = AdminFacade().apply(offset)
    if len(response) == 0:
        return make_response("Script already ran for the day.", 200)
    return make_response(f"Script succesful {int(offset) + 1}/10.", 200)


# Frontend Routing
@app.route('/')
def index():
    return render_template("index.html", page="index")


@app.route('/prospects')
def prospect_list():
    pagination = request.args.get('page') if request.args.get('page') is not None else 1
    return render_template("index.html", page="prospect_list", pagination=pagination)


@app.route('/prospects/<id>')
def prospect_page(id):
    return render_template("index.html", page="prospect", prospect_id=id)


@app.route('/draftcenter')
def draft_center():
    return render_template("index.html", page="draft_center")


@app.route('/draftsimulator')
def draft_simulator():
    return render_template("index.html", page="draft_simulator")


@app.route('/nhl/roster')
def nhl_roster():
    teams = NhlTeamService().getAllTeams()
    teams.sort(key=lambda x: x.name, reverse=False)
    return render_template("index.html", page="nhl_roster", teams=teams)


@app.route('/nhl/stats/skaters')
def nhl_stats_skater():
    return render_template("index.html", page="nhl_stats_skater")


@app.route('/nhl/fantasy')
def nhl_fantasy():
    return render_template("index.html", page="nhl_fantasy")


@app.route('/nhl/fantasy/streak')
def nhl_fantasy_streak():
    return render_template("index.html", page="nhl_fantasy_streak")


@app.route('/nhl/players')
def nhl_players():
    return render_template("index.html", page="nhl_player")


@app.route('/nhl/players/<id>')
def nhl_player_page(id):
    return render_template("index.html", page="nhl_player", player_id=id)


@app.route('/nhl/schedule')
def nhl_schedule():
    return render_template("index.html", page="nhl_schedule")


@app.route('/nhl/teams')
def nhl_teams():
    return render_template("index.html", page="nhl_teams")


# -------- API Routing -------------

def makeHttpResponse(data):
    return app.response_class(
        response=json.dumps(data, default=lambda o: o.__dict__),
        mimetype='application/json'
    )


@app.route('/api/drafts')
def getEntireDraftSimulation():
    if request.args.get('ranked') is not None and request.args.get('ranked').upper() == "TRUE":
        response = ProspectEliteService().getAllProspectsWithRanking()
    else:
        response = MockDraftSelectorServiceFacade().getEntireDraftSimulation()

    # return json.dumps([draft.__dict__ for draft in draftpicks])
    return makeHttpResponse(response)


@app.route('/api/prospects')
def getProspects():
    if request.args.get('position') is not None:
        page = request.args.get('page') if request.args.get('page') is not None else 0
        response = ProspectEliteService().getProspectByPosition(request.args.get('position'), page)
    elif request.args.get('page') is not None:
        response = ProspectEliteService().getProspectsAtPage(request.args.get('page'))
    elif request.args.get('id') is not None:
        response = ProspectEliteService().getProspectById(request.args.get('id'))
    else:
        response = ProspectEliteService().getAllProspects()

    return makeHttpResponse(response)


@app.route('/api/news')
def getTwitterNews():
    response = TwitterServiceFacade().get_hockey_tweets()
    return makeHttpResponse(response)


@app.route('/api/nhl/teams')
def getNhlTeams():
    response = NhlTeamService().getAllTeams()
    return makeHttpResponse(response)


@app.route('/api/nhl/schedule')
def getNhlSchedule():
    response = NHLScheduleService().get_current_week_games()
    return makeHttpResponse(response)


@app.route('/api/nhl/schedule/<id>')
def getNhlScheduleByTeamId(id):
    response = NHLScheduleService().get_current_week_schedule_by_teamId(id)
    return makeHttpResponse(response)


@app.route('/api/nhl/rosters/<id>')
def getNhlRoster(id):
    response = NHLRosterServiceFacade().get_nhl_roster_by_team_id(id)
    return makeHttpResponse(response)


@app.route('/api/nhl/players/<id>')
def getNhlPlayer(id):
    response = NHLPlayerServiceFacade().get_player_by_playerId_and_seasons(id)
    return makeHttpResponse(response)


@app.route('/api/nhl/players/<id>/gamelog')
def getNhlPlayerGameLog(id):
    response = GameLogService().get_player_gamelog(id)
    return makeHttpResponse(response)


@app.route('/api/nhl/stats/skaters')
def getNhlStatsSkater():
    if request.args.get('position') == 'D':
        response = NHLStatsLeaderService().getDefensemen()
    elif request.args.get('position') == 'F':
        response = NHLStatsLeaderService().getForwards()
    elif request.args.get('position') == 'G':
        response = NHLStatsLeaderService().getGoalies()
    else:
        response = NHLStatsLeaderService().getAllPlayers() \
                   + NHLStatsLeaderService().getAllPlayers(start=101, end=200) \
                   + NHLStatsLeaderService().getAllPlayers(start=201, end=300) \
                   + NHLStatsLeaderService().getAllPlayers(start=301, end=400) \
                   + NHLStatsLeaderService().getAllPlayers(start=401, end=500)
    return makeHttpResponse(response)


@app.route('/api/nhl/fantasy')
def getNhlFantasyPlayers():
    # if request.args.get('streak').lower() == 'true':
    # response = FantasyNhlPlayerFacade().getAllFantasySkatersOnHotStreak()
    if request.args.get('team') is not None:
        response = FantasyNhlPlayerService().getAllFantasySkatersWithTeamId(request.args.get('team'))
    elif request.args.get('playerName') is not None:
        response = FantasyNhlPlayerService().getAllFantasySkatersBySearchName(request.args.get('playerName'))

    else:
        positions = request.args.getlist('position')
        min_game = request.args.get('minGame')
        percentile_shot = request.args.get('shotPercentile')
        percentile_hit = request.args.get('hitPercentile')
        percentile_block = request.args.get('blockPercentile')
        percentile_goal = request.args.get('goalPercentile')
        percentile_assist = request.args.get('assistPercentile')
        percentile_point = request.args.get('pointPercentile')
        percentile_toi = request.args.get('toiPercentile')
        percentile_pptoi = request.args.get('pptoiPercentile')
        percentile_evtoi = request.args.get('evtoiPercentile')
        response = FantasyNhlPlayerFacade().getAllFantasySkaters(positions, min_game, percentile_shot,
                                                                 percentile_hit,
                                                                 percentile_block,
                                                                 percentile_goal,
                                                                 percentile_assist,
                                                                 percentile_point,
                                                                 percentile_toi,
                                                                 percentile_pptoi,
                                                                 percentile_evtoi)
    return makeHttpResponse(response)


@app.route('/api/nhl/fantasy/streak')
def getNhlFantasyPlayerStreaks():
    positions = request.args.getlist('position')
    if len(positions) > 0:
        response = FantasyPlayerStreakIndexService().getAllFantasyPlayerStreakIndexesByPositionCodes(positions)
    else:
        response = FantasyPlayerStreakIndexService().getAllFantasyPlayerStreakIndexes()
    return makeHttpResponse(response)


if __name__ == '__main__':
    # Threaded option to enable multiple instances for multiple user access support
    app.run(debug=True)
