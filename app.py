from flask import Flask, request, jsonify

app = Flask(__name__)

restaurants = {}
dishes = {}
users = {}
orders = {}
ratings = {}
feedback = []

restaurant_id_counter = 1
dish_id_counter = 1
user_id_counter = 1
order_id_counter = 1
rating_id_counter = 1

# Restaurant Module
@app.route("/api/v1/restaurants", methods=["POST"])
def register_restaurant():
    global restaurant_id_counter
    data = request.json
    if not all(k in data for k in ("name", "category", "location", "images", "contact")):
        return jsonify({"error": "Invalid data"}), 400
    for r in restaurants.values():
        if r["name"] == data["name"]:
            return jsonify({"error": "Restaurant already exists"}), 409
    restaurant = {
        "id": restaurant_id_counter,
        "name": data["name"],
        "category": data["category"],
        "location": data["location"],
        "images": data["images"],
        "contact": data["contact"],
        "enabled": True,
        "approved": False
    }
    restaurants[restaurant_id_counter] = restaurant
    restaurant_id_counter += 1
    return jsonify(restaurant), 201

@app.route("/api/v1/restaurants/<int:restaurant_id>", methods=["PUT"])
def update_restaurant(restaurant_id):
    if restaurant_id not in restaurants:
        return jsonify({"error": "Restaurant not found"}), 404
    restaurants[restaurant_id].update(request.json)
    return jsonify(restaurants[restaurant_id]), 200

@app.route("/api/v1/restaurants/<int:restaurant_id>/disable", methods=["PUT"])
def disable_restaurant(restaurant_id):
    if restaurant_id not in restaurants:
        return jsonify({"error": "Restaurant not found"}), 404
    restaurants[restaurant_id]["enabled"] = False
    return jsonify({"message": "Restaurant disabled"}), 200

@app.route("/api/v1/restaurants/<int:restaurant_id>", methods=["GET"])
def view_restaurant(restaurant_id):
    if restaurant_id not in restaurants:
        return jsonify({"error": "Restaurant not found"}), 404

    return jsonify(restaurants[restaurant_id]), 200

@app.route("/api/v1/restaurants/<int:restaurant_id>", methods=["DELETE"])
def delete_restaurant(restaurant_id):
    if restaurant_id not in restaurants:
        return jsonify({"error": "Restaurant not found"}), 404
    del restaurants[restaurant_id]
    return jsonify({"message": "Restaurant deleted"}), 200

# Dish Module
@app.route("/api/v1/restaurants/<int:restaurant_id>/dishes", methods=["POST"])
def add_dish(restaurant_id):
    global dish_id_counter
    if restaurant_id not in restaurants:
        return jsonify({"error": "Restaurant not found"}), 404
    data = request.json
    if not all(k in data for k in ("name", "type", "price", "available_time", "image")):
        return jsonify({"error": "Invalid data"}), 400
    dish = {
        "id": dish_id_counter,
        "restaurant_id": restaurant_id,
        "name": data["name"],
        "type": data["type"],
        "price": data["price"],
        "available_time": data["available_time"],
        "image": data["image"],
        "enabled": True
    }
    dishes[dish_id_counter] = dish
    dish_id_counter += 1
    return jsonify(dish), 201

@app.route("/api/v1/dishes/<int:dish_id>", methods=["PUT"])
def update_dish(dish_id):
    if dish_id not in dishes:
        return jsonify({"error": "Dish not found"}), 404
    dishes[dish_id].update(request.json)
    return jsonify(dishes[dish_id]), 200

@app.route("/api/v1/dishes/<int:dish_id>/status", methods=["PUT"])
def update_dish_status(dish_id):
    if dish_id not in dishes:
        return jsonify({"error": "Dish not found"}), 404
    data = request.json
    dishes[dish_id]["enabled"] = data.get("enabled", True)
    return jsonify({"message": "Dish status updated"}), 200

@app.route("/api/v1/dishes/<int:dish_id>", methods=["DELETE"])
def delete_dish(dish_id):
    if dish_id not in dishes:
        return jsonify({"error": "Dish not found"}), 404
    del dishes[dish_id]
    return jsonify({"message": "Dish deleted"}), 200


# Admin Module
@app.route("/api/v1/admin/restaurants/<int:restaurant_id>/approve", methods=["PUT"])
def approve_restaurant(restaurant_id):
    if restaurant_id not in restaurants:
        return jsonify({"error": "Restaurant not found"}), 404

    restaurants[restaurant_id]["approved"] = True
    return jsonify({"message": "Restaurant approved"}), 200

@app.route("/api/v1/admin/restaurants/<int:restaurant_id>/disable", methods=["PUT"])
def admin_disable_restaurant(restaurant_id):
    if restaurant_id not in restaurants:
        return jsonify({"error": "Restaurant not found"}), 404

    restaurants[restaurant_id]["enabled"] = False
    return jsonify({"message": "Restaurant disabled by admin"}), 200

@app.route("/api/v1/admin/feedback", methods=["GET"])
def view_feedback():
    return jsonify(feedback), 200

@app.route("/api/v1/admin/orders", methods=["GET"])
def view_orders():
    return jsonify(list(orders.values())), 200


#User Module
@app.route("/api/v1/users/register", methods=["POST"])
def register_user():
    global user_id_counter
    data = request.json

    for u in users.values():
        if u["email"] == data["email"]:
            return jsonify({"error": "User already exists"}), 409
    user = {
        "id": user_id_counter,
        "name": data["name"],
        "email": data["email"],
        "password": data["password"]
    }
    users[user_id_counter] = user
    user_id_counter += 1

    return jsonify(user), 201

@app.route("/api/v1/restaurants/search", methods=["GET"])
def search_restaurants():
    name = request.args.get("name", "")
    location = request.args.get("location", "")
    dish_name = request.args.get("dish", "")

    result = []

    for r in restaurants.values():
        if name.lower() in r["name"].lower() and location.lower() in r["location"].lower():
            if dish_name:
                restaurant_dishes = [d for d in dishes.values() if d["restaurant_id"] == r["id"]]
                if any(dish_name.lower() in d["name"].lower() for d in restaurant_dishes):
                    result.append(r)
            else:
                result.append(r)

    return jsonify(result), 200



# Order Module
@app.route("/api/v1/orders", methods=["POST"])
def place_order():
    global order_id_counter
    data = request.json

    if not data.get("user_id") or not data.get("restaurant_id") or not data.get("dishes"):
        return jsonify({"error": "Invalid order data"}), 400

    order = {
        "id": order_id_counter,
        "user_id": data["user_id"],
        "restaurant_id": data["restaurant_id"],
        "dishes": data["dishes"],
        "status": "Placed"
    }

    orders[order_id_counter] = order
    order_id_counter += 1

    return jsonify(order), 201


@app.route("/api/v1/restaurants/<int:restaurant_id>/orders", methods=["GET"])
def orders_by_restaurant(restaurant_id):
    result = [o for o in orders.values() if o["restaurant_id"] == restaurant_id]
    return jsonify(result), 200

@app.route("/api/v1/users/<int:user_id>/orders", methods=["GET"])
def orders_by_user(user_id):
    result = [o for o in orders.values() if o["user_id"] == user_id]
    return jsonify(result), 200


# Ratings
@app.route("/api/v1/ratings", methods=["POST"])
def give_rating():
    global rating_id_counter
    data = request.json

    if not data.get("order_id") or not data.get("rating"):
        return jsonify({"error": "Invalid rating data"}), 400

    rating = {
        "id": rating_id_counter,
        "order_id": data["order_id"],
        "rating": data["rating"],
        "comment": data.get("comment", "")
    }

    ratings[rating_id_counter] = rating
    rating_id_counter += 1

    feedback.append(rating)
    return jsonify(rating), 201
@app.route("/api/v1/admin/reset", methods=["POST"])
def reset_data():
    global restaurants, dishes, users, orders, ratings, feedback
    global restaurant_id_counter, dish_id_counter, user_id_counter, order_id_counter, rating_id_counter

    restaurants.clear()
    dishes.clear()
    users.clear()
    orders.clear()
    ratings.clear()
    feedback.clear()

    restaurant_id_counter = 1
    dish_id_counter = 1
    user_id_counter = 1
    order_id_counter = 1
    rating_id_counter = 1

    return jsonify({"message": "Data reset"}), 200


if __name__ == "__main__":
    app.run(debug=True)
