from flask import Flask, request, jsonify, render_template, redirect, jsonify
from mockdraft_selector import MockDraftSelector

from model.prospect import ProspectElite
from model.draftpick import DraftPick
from repository.prospect_elite_dao import ProspectEliteDao
from repository.prospect_dao import ProspectDao

import json

app = Flask(__name__)

# A welcome message to test our server
@app.route('/')
def index():

    prospects = ProspectEliteDao().getAllProspects()
    mockdraft = MockDraftSelector(prospects)

    draftlist = []
    for i in range(31):
        draftlist.append(mockdraft.pickPlayerBySelection(i+1))

    # draftpicks = jsonify(json.dumps([draftpick.__dict__ for draftpick in draftlist]))
    # for prospect in draftlist:
    #     print(prospect.__dict__)
    # print(draftpicks)
    return render_template("index.html", draftpicks=draftlist)

if __name__ == '__main__':
    # Threaded option to enable multiple instances for multiple user access support
    app.run(threaded=True, port=5000)
