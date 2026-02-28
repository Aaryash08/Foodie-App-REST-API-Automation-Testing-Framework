---

# 🍽️ Foodie App – REST API & Automation Testing Framework

A modular Flask-based REST API for a food ordering system with end-to-end API automation using **Pytest** and **Robot Framework**.

---

## 🚀 Tech Stack

* **Backend:** Flask, REST APIs
* **Testing:** Pytest, Robot Framework, RequestsLibrary
* **Language:** Python
* **Architecture:** Modular Blueprint-based Design
* **Reporting:** HTML Reports, XML Reports

---

## 📌 Project Overview

Foodie App is a backend-focused project that demonstrates:

* REST API development using Flask
* Modular architecture with Blueprints
* In-memory data layer simulating database behavior
* End-to-end API automation
* Positive and negative test validation
* Regression-ready test reporting

---

## 🏗️ Architecture

```
Foodie_App/
│
├── app.py                # Application entry point
├── models.py             # In-memory data layer
├── routes/
│   ├── restaurants.py
│   ├── dishes.py
│   ├── users.py
│   ├── orders.py
│   ├── ratings.py
│   └── admin.py
│
├── pytest/               # Pytest automation suite
│   └── test_api.py
│
├── Robot/                # Robot Framework tests
│   └── api_tests.robot
│
└── pytest_reports/       # Generated test reports
```

---

## 🔥 Features

### ✅ Restaurant Module

* Register restaurant
* Update & delete restaurant
* Admin approval
* Search functionality
* Duplicate validation

### ✅ Dish Module

* Add dish to restaurant
* Enable/disable dish
* Delete dish

### ✅ User Module

* User registration
* Duplicate email validation

### ✅ Order Module

* Place order
* Order validation

### ✅ Ratings & Feedback

* Submit rating
* Admin feedback retrieval

---

## 🧪 Automation Testing

### ✔ Pytest Automation

* Session-scoped fixtures
* Backend reset before execution
* 18+ automated test cases
* Positive & negative scenarios
* HTML & XML reporting support

Run Pytest:

```bash
pytest -s pytest/ --html=pytest_reports/report.html --self-contained-html --junitxml=pytest_reports/output.xml
```

---

### ✔ Robot Framework Automation

* Keyword-driven testing
* Suite-level setup & teardown
* HTML, XML execution reports
* Full regression coverage

Run Robot:

```bash
robot -d Robot_reports Robot/
```

---

## 📊 Test Coverage Includes

* Restaurant lifecycle validation
* Duplicate entry handling
* Dish management
* User registration validation
* Order placement flow
* Rating & feedback flow
* Admin moderation
* Data cleanup

---

## 🛠️ Setup Instructions

### 1️⃣ Clone Repository

```bash
git clone <your-repo-link>
cd Foodie_App
```

### 2️⃣ Create Virtual Environment

```bash
python -m venv venv
venv\Scripts\activate   # Windows
```

### 3️⃣ Install Dependencies

```bash
pip install -r requirements.txt
```

### 4️⃣ Run Backend

```bash
python app.py
```

Server runs at:

```
http://localhost:5000/api/v1
```

---

## 🎯 Learning Outcomes

* RESTful API design principles
* Modular backend architecture
* HTTP status code handling
* API automation testing best practices
* Test isolation & regression validation
* Reporting integration for CI/CD readiness

---

## 📌 Author

**Aaryash Kumar**
📧 [kumaraaryash@gmail.com](mailto:kumaraaryash@gmail.com)
🔗 LinkedIn | GitHub | LeetCode

---
