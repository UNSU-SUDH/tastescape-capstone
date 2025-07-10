from flask import Flask, request, jsonify, send_from_directory
from flask_cors import CORS
import mysql.connector
import os

app = Flask(__name__, static_folder=".", static_url_path="")
CORS(app)

# MySQL connection
db = mysql.connector.connect(
    host="localhost",
    user="root",  # ✅ Replace with your actual MySQL username
    password="unsu@123",  # ✅ Replace with your actual MySQL password
    database="tastescape"
)
cursor = db.cursor(dictionary=True)

@app.route("/")
def serve_frontend():
    return send_from_directory(app.static_folder, "index.html")

@app.route("/reviews", methods=["POST"])
def add_review():
    data = request.get_json()
    user = data.get("user")
    rating = data.get("rating")
    comment = data.get("comment")
    restaurant_name = user  # use user field as restaurant name

    # Check if restaurant exists
    cursor.execute("SELECT id FROM restaurants WHERE name = %s", (restaurant_name,))
    result = cursor.fetchone()
    if result:
        restaurant_id = result["id"]
    else:
        cursor.execute("INSERT INTO restaurants (name) VALUES (%s)", (restaurant_name,))
        db.commit()
        restaurant_id = cursor.lastrowid

    # Insert review
    cursor.execute(
        "INSERT INTO reviews (restaurant_id, user, rating, comment) VALUES (%s, %s, %s, %s)",
        (restaurant_id, restaurant_name, rating, comment)
    )
    db.commit()
    return jsonify({"status": "added", "restaurant_id": restaurant_id})

@app.route("/reviews/<int:restaurant_id>", methods=["GET"])
def get_reviews(restaurant_id):
    cursor.execute("SELECT * FROM reviews WHERE restaurant_id = %s", (restaurant_id,))
    return jsonify(cursor.fetchall())

@app.route("/reviews", methods=["GET"])
def get_all_reviews():
    cursor.execute("""
        SELECT r.user, r.rating, r.comment, res.name AS restaurant
        FROM reviews r
        JOIN restaurants res ON r.restaurant_id = res.id
    """)
    return jsonify(cursor.fetchall())

# --- Run the app on the correct port (for Render) ---
if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5000))
    app.run(host="0.0.0.0", port=port)
