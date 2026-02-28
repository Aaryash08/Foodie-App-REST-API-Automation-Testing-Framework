from flask import Blueprint, request, jsonify
import models

ratings_bp = Blueprint("ratings", __name__)

@ratings_bp.route("/api/v1/ratings", methods=["POST"])
def give_rating():
    data = request.json

    if not data.get("order_id") or not data.get("rating"):
        return jsonify({"error": "Invalid rating data"}), 400

    rating = {
        "id": models.rating_id_counter,
        "order_id": data["order_id"],
        "rating": data["rating"],
        "comment": data.get("comment", "")
    }

    models.ratings[models.rating_id_counter] = rating
    models.feedback.append(rating)
    models.rating_id_counter += 1

    return jsonify(rating), 201