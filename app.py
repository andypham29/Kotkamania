from flask import Flask, request, jsonify, render_template, redirect, jsonify

from server.service.facade.mockdraft_selector_service_facade import MockDraftSelectorServiceFacade
from helper.http_helper import HttpHelper

from server.model.draftpick import DraftPick

import json

app = Flask(__name__)

# A welcome message to test our server
@app.route('/')
def index():
    draftpicks = HttpHelper.get(request.base_url + "drafts")

    return render_template("index.html", draftpicks=draftpicks)

@app.route('/drafts')
def getEntireDraftSimulation():
    draftpicks = MockDraftSelectorServiceFacade(50).getEntireDraftSimulation()

    # return json.dumps([draft.__dict__ for draft in draftpicks])
    return json.dumps(draftpicks, default=lambda o: o.__dict__)

if __name__ == '__main__':
    # Threaded option to enable multiple instances for multiple user access support
    app.run(threaded=True, port=5000)
