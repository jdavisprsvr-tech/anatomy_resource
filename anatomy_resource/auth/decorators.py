from functools import wraps

from flask import jsonify
from flask_jwt_extended import verify_jwt_in_request, get_jwt_identity

from ..extensions import db
from .models import User


def content_editor_required(fn):
    @wraps(fn)
    def wrapper(*args, **kwargs):
        verify_jwt_in_request()

        user_id = get_jwt_identity()
        user = db.session.get(User, int(user_id))

        if not user:
            return jsonify({"error": "User not found"}), 404

        if user.role != "content_editor":
            return jsonify({"error": "Content Editor access required"}), 403

        return fn(*args, **kwargs)

    return wrapper