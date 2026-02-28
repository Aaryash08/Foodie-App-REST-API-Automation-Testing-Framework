from flask import Flask, jsonify
from routes.restaurants import restaurants_bp
from routes.dishes import dishes_bp
from routes.users import users_bp
from routes.orders import orders_bp
from routes.admin import admin_bp
from routes.ratings import ratings_bp
import models

app = Flask(__name__)

# Register Blueprints
app.register_blueprint(restaurants_bp)
app.register_blueprint(dishes_bp)
app.register_blueprint(users_bp)
app.register_blueprint(orders_bp)
app.register_blueprint(admin_bp)
app.register_blueprint(ratings_bp)


@app.route("/api/v1/admin/reset", methods=["POST"])
def reset_data():
    models.restaurants.clear()
    models.dishes.clear()
    models.users.clear()
    models.orders.clear()
    models.ratings.clear()
    models.feedback.clear()

    models.restaurant_id_counter = 1
    models.dish_id_counter = 1
    models.user_id_counter = 1
    models.order_id_counter = 1
    models.rating_id_counter = 1

    return jsonify({"message": "Data reset"}), 200


if __name__ == "__main__":
    app.run(debug=True)