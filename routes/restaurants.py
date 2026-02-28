from flask import Blueprint, request, jsonify
import models

restaurants_bp = Blueprint("restaurants", __name__)

@restaurants_bp.route("/api/v1/restaurants", methods=["POST"])
def register_restaurant():
    data = request.json

    if not all(k in data for k in ("name", "category", "location", "images", "contact")):
        return jsonify({"error": "Invalid data"}), 400

    for r in models.restaurants.values():
        if r["name"] == data["name"]:
            return jsonify({"error": "Restaurant already exists"}), 409

    restaurant = {
        "id": models.restaurant_id_counter,
        "name": data["name"],
        "category": data["category"],
        "location": data["location"],
        "images": data["images"],
        "contact": data["contact"],
        "enabled": True,
        "approved": False
    }

    models.restaurants[models.restaurant_id_counter] = restaurant
    models.restaurant_id_counter += 1
    return jsonify(restaurant), 201


@restaurants_bp.route("/api/v1/restaurants/<int:restaurant_id>", methods=["PUT"])
def update_restaurant(restaurant_id):
    if restaurant_id not in models.restaurants:
        return jsonify({"error": "Restaurant not found"}), 404

    models.restaurants[restaurant_id].update(request.json)
    return jsonify(models.restaurants[restaurant_id]), 200


@restaurants_bp.route("/api/v1/restaurants/<int:restaurant_id>/disable", methods=["PUT"])
def disable_restaurant(restaurant_id):
    if restaurant_id not in models.restaurants:
        return jsonify({"error": "Restaurant not found"}), 404

    models.restaurants[restaurant_id]["enabled"] = False
    return jsonify({"message": "Restaurant disabled"}), 200


@restaurants_bp.route("/api/v1/restaurants/<int:restaurant_id>", methods=["GET"])
def view_restaurant(restaurant_id):
    if restaurant_id not in models.restaurants:
        return jsonify({"error": "Restaurant not found"}), 404
    return jsonify(models.restaurants[restaurant_id]), 200


@restaurants_bp.route("/api/v1/restaurants/<int:restaurant_id>", methods=["DELETE"])
def delete_restaurant(restaurant_id):
    if restaurant_id not in models.restaurants:
        return jsonify({"error": "Restaurant not found"}), 404

    del models.restaurants[restaurant_id]
    return jsonify({"message": "Restaurant deleted"}), 200


@restaurants_bp.route("/api/v1/restaurants/search", methods=["GET"])
def search_restaurants():
    name = request.args.get("name", "")
    location = request.args.get("location", "")
    dish_name = request.args.get("dish", "")

    result = []

    for r in models.restaurants.values():
        if name.lower() in r["name"].lower() and location.lower() in r["location"].lower():
            if dish_name:
                restaurant_dishes = [d for d in models.dishes.values() if d["restaurant_id"] == r["id"]]
                if any(dish_name.lower() in d["name"].lower() for d in restaurant_dishes):
                    result.append(r)
            else:
                result.append(r)

    return jsonify(result), 200