from functools import wraps

from flask import jsonify, g
from flask_jwt_extended import verify_jwt_in_request, get_jwt_identity

from ..extensions import db
from .models import User


def token_required(fn):
    @wraps(fn)
    def wrapper(*args, **kwargs):
        verify_jwt_in_request()

        identity = get_jwt_identity()

        try:
            user_id = int(identity)
        except (TypeError, ValueError):
            return jsonify({"error": "Invalid token identity"}), 401

        g.current_user_id = user_id

        return fn(*args, **kwargs)

    return wrapper


def content_editor_required(fn):
    @wraps(fn)
    @token_required
    def wrapper(*args, **kwargs):
        user = db.session.get(User, g.current_user_id)

        if not user:
            return jsonify({"error": "User not found"}), 404

        if user.role != "content_editor":
            return jsonify({
                "error": "Content Editor access required"
            }), 403

        return fn(*args, **kwargs)

    return wrapper