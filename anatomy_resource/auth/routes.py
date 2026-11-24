import secrets
from sqlalchemy.exc import IntegrityError
from flask import Blueprint, request, jsonify, current_app
from flask_jwt_extended import create_access_token
from flask import g
from .decorators import token_required
from ..extensions import db
from . import auth_bp
from .models import User






@auth_bp.post("/register")
def register():
    data = request.get_json(silent=True)

    if not isinstance(data, dict):
        return jsonify({
            "code": "VALIDATION_ERROR",
            "message": "A valid JSON object is required"
        }), 400

    username = data.get("username")
    email = data.get("email")
    password = data.get("password")

    if not isinstance(username, str) or not username.strip():
        return jsonify({
            "code": "VALIDATION_ERROR",
            "message": "username is required"
        }), 400

    if not isinstance(email, str) or not email.strip():
        return jsonify({
            "code": "VALIDATION_ERROR",
            "message": "email is required"
        }), 400

    if not isinstance(password, str) or not password:
        return jsonify({
            "code": "VALIDATION_ERROR",
            "message": "password is required"
        }), 400

    username = username.strip()
    email = email.strip().lower()

    if not 3 <= len(username) <= 80:
        return jsonify({
            "code": "VALIDATION_ERROR",
            "message": "username must be between 3 and 80 characters"
        }), 400

    if len(email) > 120 or "@" not in email:
        return jsonify({
            "code": "VALIDATION_ERROR",
            "message": "email must be valid and no longer than 120 characters"
        }), 400

    if not 8 <= len(password) <= 128:
        return jsonify({
            "code": "VALIDATION_ERROR",
            "message": "password must be between 8 and 128 characters"
        }), 400

    existing_user = User.query.filter(
        (User.username == username) | (User.email == email)
    ).first()

    if existing_user:
        if existing_user.username == username:
            message = "username already in use"
        else:
            message = "email already in use"

        return jsonify({
            "code": "CONFLICT",
            "message": message
        }), 409

    user = User(username=username, email=email)
    user.set_password(password)

    db.session.add(user)
    db.session.commit()

    return jsonify({
        "id": user.id,
        "username": user.username,
        "email": user.email,
        "role": user.role,
        "created_at": user.created_at.isoformat()
    }), 201



@auth_bp.post("/admin_register")
def admin_register():
    expected_code = current_app.config.get("CONTENT_EDITOR_INVITE_CODE")

    if not expected_code:
        return jsonify({
            "code": "SERVICE_UNAVAILABLE",
            "message": "Editor registration is unavailable"
        }), 503

    data = request.get_json(silent=True)

    if not isinstance(data, dict):
        return jsonify({
            "code": "VALIDATION_ERROR",
            "message": "A valid JSON object is required"
        }), 400

    invite_code = data.get("invite_code")

    if not isinstance(invite_code, str) or not secrets.compare_digest(
        invite_code, expected_code
    ):
        return jsonify({
            "code": "INVALID_INVITE_CODE",
            "message": "Invalid invitation code"
        }), 403

    username = data.get("username")
    email = data.get("email")
    password = data.get("password")

    if not isinstance(username, str) or not username.strip():
        return jsonify({
            "code": "VALIDATION_ERROR",
            "message": "username is required"
        }), 400

    if not isinstance(email, str) or not email.strip():
        return jsonify({
            "code": "VALIDATION_ERROR",
            "message": "email is required"
        }), 400

    if not isinstance(password, str) or not password:
        return jsonify({
            "code": "VALIDATION_ERROR",
            "message": "password is required"
        }), 400

    username = username.strip()
    email = email.strip().lower()

    if not 3 <= len(username) <= 80:
        return jsonify({
            "code": "VALIDATION_ERROR",
            "message": "username must be between 3 and 80 characters"
        }), 400

    if len(email) > 120 or "@" not in email:
        return jsonify({
            "code": "VALIDATION_ERROR",
            "message": "email must be valid and no longer than 120 characters"
        }), 400

    if not 8 <= len(password) <= 128:
        return jsonify({
            "code": "VALIDATION_ERROR",
            "message": "password must be between 8 and 128 characters"
        }), 400

    existing_user = User.query.filter(
        (User.username == username) | (User.email == email)
    ).first()

    if existing_user:
        if existing_user.username == username:
            message = "username already in use"
        else:
            message = "email already in use"

        return jsonify({
            "code": "CONFLICT",
            "message": message
        }), 409

    user = User(
        username=username,
        email=email,
        role="content_editor"
    )
    user.set_password(password)

    db.session.add(user)
    db.session.commit()

    return jsonify({
        "id": user.id,
        "username": user.username,
        "email": user.email,
        "role": user.role,
        "created_at": user.created_at.isoformat()
    }), 201



@auth_bp.post("/login")
def login():
    data = request.get_json(silent=True) or {}

    email = data.get("email", "").strip().lower()
    password = data.get("password", "")

    if not email or not password:
        return jsonify({"error": "Email and password are required"}), 400

    user = User.query.filter_by(email=email).first()

    if not user or not user.check_password(password):
        return jsonify({"error": "Invalid email or password"}), 401

    access_token = create_access_token(
        identity=str(user.id),
        additional_claims={"role": user.role}
    )

    return jsonify({
        "access_token": access_token,
        "user": {
            "id": user.id,
            "username": user.username,
            "email": user.email,
            "role": user.role,
        },
    }), 200


@auth_bp.get("/me")
@token_required
def get_current_user():
    user = db.session.get(User, g.current_user_id)

    if not user:
        return jsonify({"error": "User not found"}), 404

    return jsonify({
        "id": user.id,
        "username": user.username,
        "email": user.email,
        "role": user.role,
    }), 200





@auth_bp.patch("/me")
@token_required
def update_current_user():
    user = db.session.get(User, g.current_user_id)

    if not user:
        return jsonify({
            "code": "NOT_FOUND",
            "message": "User not found"
        }), 404

    data = request.get_json(silent=True)

    if not isinstance(data, dict):
        return jsonify({
            "code": "VALIDATION_ERROR",
            "message": "A valid JSON object is required"
        }), 400

    allowed_fields = {"username", "email"}
    unexpected_fields = set(data.keys()) - allowed_fields

    if unexpected_fields:
        return jsonify({
            "code": "VALIDATION_ERROR",
            "message": "Only username and email can be updated"
        }), 400

    if "username" in data:
        username = data["username"]

        if not isinstance(username, str) or not username.strip():
            return jsonify({
                "code": "VALIDATION_ERROR",
                "message": "username must be a non-empty string"
            }), 400

        username = username.strip()

        if not 3 <= len(username) <= 80:
            return jsonify({
                "code": "VALIDATION_ERROR",
                "message": "username must be between 3 and 80 characters"
            }), 400

        existing_user = User.query.filter(
            User.username == username,
            User.id != g.current_user_id
        ).first()

        if existing_user:
            return jsonify({
                "code": "CONFLICT",
                "message": "username already in use"
            }), 409

        user.username = username

    if "email" in data:
        email = data["email"]

        if not isinstance(email, str) or not email.strip():
            return jsonify({
                "code": "VALIDATION_ERROR",
                "message": "email must be a non-empty string"
            }), 400

        email = email.strip().lower()

        if len(email) > 120 or "@" not in email:
            return jsonify({
                "code": "VALIDATION_ERROR",
                "message": "email must be valid and no longer than 120 characters"
            }), 400

        existing_user = User.query.filter(
            User.email == email,
            User.id != g.current_user_id
        ).first()

        if existing_user:
            return jsonify({
                "code": "CONFLICT",
                "message": "email already in use"
            }), 409

        user.email = email

    if data:
        try:
            db.session.commit()
        except IntegrityError:
            db.session.rollback()
            return jsonify({
                "code": "CONFLICT",
                "message": "Username or email already in use"
            }), 409

    return jsonify({
        "id": user.id,
        "username": user.username,
        "email": user.email,
        "role": user.role,
    }), 200


@auth_bp.get("/editor-dashboard")
@token_required
def editor_dashboard():
    user = db.session.get(User, g.current_user_id)

    if not user:
        return jsonify({
            "code": "NOT_FOUND",
            "message": "User not found"
        }), 404

    if user.role != "content_editor":
        return jsonify({
            "code": "FORBIDDEN",
            "message": "Content editor access required"
        }), 403

    return jsonify({
        "message": "Welcome to the content editor dashboard",
        "user_id": user.id,
        "role": user.role
    }), 200
