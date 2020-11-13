import json

from flask import Flask, request, render_template

from server.mockdraft.service.facade.mockdraft_selector_service_facade import MockDraftSelectorServiceFacade
from server.mockdraft.service.prospect_elite_service import ProspectEliteService
from server.nhlapi.service.facade.nhl_player_service_facade import NHLPlayerServiceFacade
from server.nhlapi.service.facade.nhl_roster_service_facade import NHLRosterServiceFacade
from server.nhlapi.service.nhl_stats_leader_service import NHLStatsLeaderService
from server.nhlapi.service.nhl_team_service import NhlTeamService
from server.twitterapi.service.facade.twitter_service_facade import TwitterServiceFacade

app = Flask(__name__)


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


@app.route('/nhl/stats/skater')
def nhl_stats_skater():
    return render_template("index.html", page="nhl_stats_skater")


# -------- API Routing -------------
@app.route('/api/drafts')
def getEntireDraftSimulation():
    if request.args.get('ranked') is not None and request.args.get('ranked').upper() == "TRUE":
        response = ProspectEliteService().getAllProspectsWithRanking()
    else:
        response = MockDraftSelectorServiceFacade().getEntireDraftSimulation()

    # return json.dumps([draft.__dict__ for draft in draftpicks])
    return json.dumps(response, default=lambda o: o.__dict__)


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

    return json.dumps(response, default=lambda o: o.__dict__)


@app.route('/api/news')
def getTwitterNews():
    response = TwitterServiceFacade().get_hockey_tweets()
    return json.dumps(response, default=lambda o: o.__dict__)


@app.route('/api/nhl/rosters/<id>')
def getNhlRoster(id):
    response = NHLRosterServiceFacade().get_nhl_roster_by_team_id(id)
    return json.dumps(response, default=lambda o: o.__dict__)


@app.route('/api/nhl/players/<id>')
def getNhlPlayer(id):
    response = NHLPlayerServiceFacade().get_player_stats_by_playerId_and_seasons(id,
                                                                                 ["20192020", "20182019", "20172018"])
    return json.dumps(response, default=lambda o: o.__dict__)


@app.route('/api/nhl/stats/skaters')
def getNhlStatsSkater():
    response = NHLStatsLeaderService().getAllPlayers() \
               + NHLStatsLeaderService().getAllPlayers(start=101, end=200) \
               + NHLStatsLeaderService().getAllPlayers(start=201, end=300) \
               + NHLStatsLeaderService().getAllPlayers(start=301, end=400) \
               + NHLStatsLeaderService().getAllPlayers(start=401, end=500)
    return json.dumps(response, default=lambda o: o.__dict__)


if __name__ == '__main__':
    # Threaded option to enable multiple instances for multiple user access support
    app.run(debug=True)
