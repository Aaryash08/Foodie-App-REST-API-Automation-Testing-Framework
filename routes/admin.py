from flask import Blueprint, jsonify
import models

admin_bp = Blueprint("admin", __name__)

@admin_bp.route("/api/v1/admin/restaurants/<int:restaurant_id>/approve", methods=["PUT"])
def approve_restaurant(restaurant_id):
    if restaurant_id not in models.restaurants:
        return jsonify({"error": "Restaurant not found"}), 404

    models.restaurants[restaurant_id]["approved"] = True
    return jsonify({"message": "Restaurant approved"}), 200


@admin_bp.route("/api/v1/admin/restaurants/<int:restaurant_id>/disable", methods=["PUT"])
def admin_disable_restaurant(restaurant_id):
    if restaurant_id not in models.restaurants:
        return jsonify({"error": "Restaurant not found"}), 404

    models.restaurants[restaurant_id]["enabled"] = False
    return jsonify({"message": "Restaurant disabled by admin"}), 200


@admin_bp.route("/api/v1/admin/feedback", methods=["GET"])
def view_feedback():
    return jsonify(models.feedback), 200


@admin_bp.route("/api/v1/admin/orders", methods=["GET"])
def view_orders():
    return jsonify(list(models.orders.values())), 200