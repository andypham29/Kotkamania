from flask import Flask, request, jsonify, render_template, redirect, jsonify
from flask_api import status

from server.service.facade.mockdraft_selector_service_facade import MockDraftSelectorServiceFacade
from server.service.prospect_elite_service import ProspectEliteService
from helper.http_helper import HttpHelper

from server.model.draftpick import DraftPick

import json

app = Flask(__name__)

@app.route('/')
def index():
    return render_template("index.html")

@app.route('/api/drafts')
def getEntireDraftSimulation():
    response = None
    if request.args.get('ranked') is not None and request.args.get('ranked').upper() == "TRUE":
        response = ProspectEliteService().getAllProspectsWithRanking()
    else:
        response = MockDraftSelectorServiceFacade().getEntireDraftSimulation()

    # return json.dumps([draft.__dict__ for draft in draftpicks])
    return json.dumps(response, default=lambda o: o.__dict__)

@app.route('/api/prospects')
def getProspects():

    response = response = ProspectEliteService().getAllProspects()
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

if __name__ == '__main__':
    # Threaded option to enable multiple instances for multiple user access support
    app.run(threaded=True, port=5000)
