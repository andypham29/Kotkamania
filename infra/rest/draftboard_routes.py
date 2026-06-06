from flask import Blueprint, request, jsonify
from werkzeug.exceptions import BadRequest, NotFound

from domain.draftboard.model.domain_draftboard import DomainDraftboard

draftboard_bp = Blueprint("draftboard", __name__)

def init_draftboard_routes(service):

    @draftboard_bp.get("/draftboards/<draftboard_id>")
    def get_draftboard(draftboard_id):
        draftboard = service.get_by_id(draftboard_id)
        if draftboard is None:
            raise NotFound(f"Draftboard '{draftboard_id}' not found")
        return jsonify(draftboard.to_dict()), 200

    @draftboard_bp.post("/draftboards")
    def save_draftboard():
        try:
            payload = request.get_json(force=True)
        except Exception:
            raise BadRequest("Invalid JSON")

        draftboard = DomainDraftboard.from_dict(payload)
        service.save(draftboard)
        return jsonify({"status": "ok", "id": draftboard.id}), 201

    return draftboard_bp
