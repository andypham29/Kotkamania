from flask import Flask, request, render_template

from server.mockdraft.service.facade.mockdraft_selector_service_facade import MockDraftSelectorServiceFacade
from server.mockdraft.service.prospect_elite_service import ProspectEliteService

import json

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


if __name__ == '__main__':
    # Threaded option to enable multiple instances for multiple user access support
    app.run(debug=True)
