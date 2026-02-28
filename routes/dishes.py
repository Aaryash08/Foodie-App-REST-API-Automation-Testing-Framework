from flask import Blueprint, request, jsonify
import models

dishes_bp = Blueprint("dishes", __name__)

@dishes_bp.route("/api/v1/restaurants/<int:restaurant_id>/dishes", methods=["POST"])
def add_dish(restaurant_id):
    if restaurant_id not in models.restaurants:
        return jsonify({"error": "Restaurant not found"}), 404

    data = request.json
    if not all(k in data for k in ("name", "type", "price", "available_time", "image")):
        return jsonify({"error": "Invalid data"}), 400

    dish = {
        "id": models.dish_id_counter,
        "restaurant_id": restaurant_id,
        "name": data["name"],
        "type": data["type"],
        "price": data["price"],
        "available_time": data["available_time"],
        "image": data["image"],
        "enabled": True
    }

    models.dishes[models.dish_id_counter] = dish
    models.dish_id_counter += 1
    return jsonify(dish), 201


@dishes_bp.route("/api/v1/dishes/<int:dish_id>", methods=["PUT"])
def update_dish(dish_id):
    if dish_id not in models.dishes:
        return jsonify({"error": "Dish not found"}), 404

    models.dishes[dish_id].update(request.json)
    return jsonify(models.dishes[dish_id]), 200


@dishes_bp.route("/api/v1/dishes/<int:dish_id>/status", methods=["PUT"])
def update_dish_status(dish_id):
    if dish_id not in models.dishes:
        return jsonify({"error": "Dish not found"}), 404

    data = request.json
    models.dishes[dish_id]["enabled"] = data.get("enabled", True)
    return jsonify({"message": "Dish status updated"}), 200


@dishes_bp.route("/api/v1/dishes/<int:dish_id>", methods=["DELETE"])
def delete_dish(dish_id):
    if dish_id not in models.dishes:
        return jsonify({"error": "Dish not found"}), 404

    del models.dishes[dish_id]
    return jsonify({"message": "Dish deleted"}), 200