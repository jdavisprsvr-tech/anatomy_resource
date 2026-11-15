
from flask import Blueprint, request, jsonify
from flask_jwt_extended import jwt_required

from ..extensions import db
from ..auth.decorators import content_editor_required
from .models import AnatomyEntry


anatomy_bp = Blueprint("anatomy", __name__, url_prefix="/anatomy_entries")


def entry_to_dict(entry):
    return {
        "id": entry.id,
        "title": entry.title,
        "description": entry.description,
        "body_system": entry.body_system,
        "is_published": entry.is_published,
    }


# PUBLIC: List published anatomy entries
@anatomy_bp.get("/")
def get_entries():
    entries = AnatomyEntry.query.filter_by(
        is_published=True
    ).all()

    return jsonify([entry_to_dict(entry) for entry in entries]), 200


# PUBLIC: Get one published anatomy entry
@anatomy_bp.get("/<int:entry_id>")
def get_entry(entry_id):
    entry = AnatomyEntry.query.filter_by(
        id=entry_id,
        is_published=True
    ).first()

    if not entry:
        return jsonify({"error": "Anatomy entry not found"}), 404

    return jsonify(entry_to_dict(entry)), 200


# CONTENT EDITOR ONLY: Create an anatomy entry
@anatomy_bp.post("/")
@content_editor_required
def create_entry():
    data = request.get_json(silent=True) or {}

    title = data.get("title")
    description = data.get("description")
    body_system = data.get("body_system")
    is_published = data.get("is_published", False)

    if not all([
        isinstance(title, str) and title.strip(),
        isinstance(description, str) and description.strip(),
        isinstance(body_system, str) and body_system.strip(),
    ]):
        return jsonify({"error": "Title, description, and body system are required"}), 400

    if not isinstance(is_published, bool):
        return jsonify({"error": "is_published must be true or false"}), 400

    entry = AnatomyEntry(
        title=title.strip(),
        description=description.strip(),
        body_system=body_system.strip(),
        is_published=is_published,
    )

    db.session.add(entry)
    db.session.commit()

    return jsonify(entry_to_dict(entry)), 201


# CONTENT EDITOR ONLY: Update an anatomy entry
@anatomy_bp.put("/<int:entry_id>")
@content_editor_required
def update_entry(entry_id):
    entry = db.session.get(AnatomyEntry, entry_id)

    if not entry:
        return jsonify({"error": "Anatomy entry not found"}), 404

    data = request.get_json(silent=True) or {}

    for field in ("title", "description", "body_system"):
        if field in data:
            value = data[field]

            if not isinstance(value, str) or not value.strip():
                return jsonify({"error": f"{field} must be a non-empty string"}), 400

            setattr(entry, field, value.strip())

    if "is_published" in data:
        if not isinstance(data["is_published"], bool):
            return jsonify({"error": "is_published must be true or false"}), 400

        entry.is_published = data["is_published"]

    db.session.commit()

    return jsonify(entry_to_dict(entry)), 200


# CONTENT EDITOR ONLY: Delete an anatomy entry
@anatomy_bp.delete("/<int:entry_id>")
@content_editor_required
def delete_entry(entry_id):
    entry = db.session.get(AnatomyEntry, entry_id)

    if not entry:
        return jsonify({"error": "Anatomy entry not found"}), 404

    db.session.delete(entry)
    db.session.commit()

    return "", 204
