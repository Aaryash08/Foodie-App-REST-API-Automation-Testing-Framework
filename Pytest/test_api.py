import pytest
import requests
import uuid


BASE_URL = "http://localhost:5000/api/v1"

RESTAURANT_DATA = {
    "name": "Spice Garden",
    "category": "Indian",
    "location": "North",
    "images": [],
    "contact": "98765"
}

USER_DATA = {
    "name": "John Doe",
    "email": f"john_{uuid.uuid4().hex[:6]}@example.com",
    "password": "secret123"
}

DISH_DATA = {
    "name": "Paneer Tikka",
    "type": "Veg",
    "price": 15.0,
    "available_time": "All Day",
    "image": "paneer.jpg"
}


@pytest.fixture(scope="session")
def session():
    return requests.Session()


@pytest.fixture(scope="session")
def ids():
    return {}


def test_register_restaurant(session, ids):
    res = session.post(f"{BASE_URL}/restaurants", json=RESTAURANT_DATA)
    assert res.status_code == 201
    ids["restaurant_id"] = res.json()["id"]


def test_update_restaurant(session, ids):
    res = session.put(
        f"{BASE_URL}/restaurants/{ids['restaurant_id']}",
        json={"location": "South"}
    )
    assert res.status_code == 200
    assert res.json()["location"] == "South"


def test_approve_restaurant(session, ids):
    res = session.put(f"{BASE_URL}/admin/restaurants/{ids['restaurant_id']}/approve")
    assert res.status_code == 200


def test_add_dish(session, ids):
    res = session.post(
        f"{BASE_URL}/restaurants/{ids['restaurant_id']}/dishes",
        json=DISH_DATA
    )
    assert res.status_code == 201
    ids["dish_id"] = res.json()["id"]


def test_update_dish_status(session, ids):
    res = session.put(
        f"{BASE_URL}/dishes/{ids['dish_id']}/status",
        json={"enabled": False}
    )
    assert res.status_code == 200


def test_register_user(session, ids):
    res = session.post(f"{BASE_URL}/users/register", json=USER_DATA)
    assert res.status_code == 201
    ids["user_id"] = res.json()["id"]


def test_search_restaurant(session):
    res = session.get(f"{BASE_URL}/restaurants/search", params={"name": "Spice", "location": "South"})
    assert res.status_code == 200
    assert len(res.json()) > 0


def test_place_order(session, ids):
    payload = {
        "user_id": ids["user_id"],
        "restaurant_id": ids["restaurant_id"],
        "dishes": [ids["dish_id"]]
    }
    res = session.post(f"{BASE_URL}/orders", json=payload)
    assert res.status_code == 201
    ids["order_id"] = res.json()["id"]


def test_submit_rating(session, ids):
    payload = {
        "order_id": ids["order_id"],
        "rating": 5,
        "comment": "Excellent food!"
    }
    res = session.post(f"{BASE_URL}/ratings", json=payload)
    assert res.status_code == 201


def test_view_admin_feedback(session):
    res = session.get(f"{BASE_URL}/admin/feedback")
    assert res.status_code == 200
    assert len(res.json()) > 0


def test_delete_dish(session, ids):
    res = session.delete(f"{BASE_URL}/dishes/{ids['dish_id']}")
    assert res.status_code == 200


def test_delete_restaurant(session, ids):
    res = session.delete(f"{BASE_URL}/restaurants/{ids['restaurant_id']}")
    assert res.status_code == 200

@pytest.fixture(scope="session", autouse=True)
def reset_backend(session):
    session.post(f"{BASE_URL}/admin/reset")