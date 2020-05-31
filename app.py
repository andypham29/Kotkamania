from flask import Flask, request, jsonify, render_template, redirect, jsonify

from server.service.facade.mockdraft_selector_service_facade import MockDraftSelectorServiceFacade
from server.service.prospect_elite_service import ProspectEliteService
from helper.http_helper import HttpHelper

from server.model.draftpick import DraftPick

import json

app = Flask(__name__)

@app.route('/')
def index():
    draftpicks = HttpHelper.get(request.base_url + "api/drafts")

    return render_template("index.html", draftpicks=draftpicks)

@app.route('/api/drafts')
def getEntireDraftSimulation():
    draftpicks = MockDraftSelectorServiceFacade().getEntireDraftSimulation()

    # return json.dumps([draft.__dict__ for draft in draftpicks])
    return json.dumps(draftpicks, default=lambda o: o.__dict__)

@app.route('/api/prospects')
def getProspects():
    prospects = None
    if request.args.get('page') is not None:
        prospects = ProspectEliteService().getProspectsAtPage(int(request.args.get('page')))
    elif request.args.get('id') is not None:
        prospects = ProspectEliteService().getProspectById(int(request.args.get('id')))
    else:
        prospects = ProspectEliteService().getAllProspects()

    return json.dumps(prospects, default=lambda o: o.__dict__)

if __name__ == '__main__':
    # Threaded option to enable multiple instances for multiple user access support
    app.run(threaded=True, port=5000)
