from flask import Blueprint, request, jsonify
import models

orders_bp = Blueprint("orders", __name__)

@orders_bp.route("/api/v1/orders", methods=["POST"])
def place_order():
    data = request.json

    if not data.get("user_id") or not data.get("restaurant_id") or not data.get("dishes"):
        return jsonify({"error": "Invalid order data"}), 400

    order = {
        "id": models.order_id_counter,
        "user_id": data["user_id"],
        "restaurant_id": data["restaurant_id"],
        "dishes": data["dishes"],
        "status": "Placed"
    }

    models.orders[models.order_id_counter] = order
    models.order_id_counter += 1
    return jsonify(order), 201


@orders_bp.route("/api/v1/restaurants/<int:restaurant_id>/orders", methods=["GET"])
def orders_by_restaurant(restaurant_id):
    result = [o for o in models.orders.values() if o["restaurant_id"] == restaurant_id]
    return jsonify(result), 200


@orders_bp.route("/api/v1/users/<int:user_id>/orders", methods=["GET"])
def orders_by_user(user_id):
    result = [o for o in models.orders.values() if o["user_id"] == user_id]
    return jsonify(result), 200