from flask import Blueprint, request, jsonify
import models

users_bp = Blueprint("users", __name__)

@users_bp.route("/api/v1/users/register", methods=["POST"])
def register_user():
    data = request.json

    for u in models.users.values():
        if u["email"] == data["email"]:
            return jsonify({"error": "User already exists"}), 409

    user = {
        "id": models.user_id_counter,
        "name": data["name"],
        "email": data["email"],
        "password": data["password"]
    }

    models.users[models.user_id_counter] = user
    models.user_id_counter += 1
    return jsonify(user), 201