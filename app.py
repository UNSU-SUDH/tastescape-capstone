from flask import Flask, request, jsonify
from flask_cors import CORS
import mysql.connector

app = Flask(__name__)
CORS(app)


db = mysql.connector.connect(
    host="localhost",
    user="root",
    password="unsu@123",  # <-- Change this to your actual MySQL password
    database="tastescape"
)
cursor = db.cursor(dictionary=True)

# ✅ Get all restaurants
@app.route('/api/restaurants', methods=['GET'])
def get_restaurants():
    cursor.execute("SELECT * FROM restaurants")
    return jsonify(cursor.fetchall())

# ✅ Add a new restaurant
@app.route('/api/restaurants', methods=['POST'])
def add_restaurant():
    data = request.json
    print("Adding restaurant:", data)
    cursor.execute("INSERT INTO restaurants (name) VALUES (%s)", (data['name'],))
    db.commit()
    return jsonify({'status': 'added'})

# ✅ Get reviews for a restaurant
@app.route('/api/reviews/<int:restaurant_id>', methods=['GET'])
def get_reviews(restaurant_id):
    cursor.execute("SELECT * FROM reviews WHERE restaurant_id = %s", (restaurant_id,))
    return jsonify(cursor.fetchall())

# ✅ Add a review
@app.route('/api/reviews', methods=['POST'])
def add_review():
    data = request.json
    print("Adding review:", data)
    cursor.execute("INSERT INTO reviews (restaurant_id, user, rating, comment) VALUES (%s, %s, %s, %s)",
                   (data['restaurant_id'], data['user'], data['rating'], data['comment']))
    db.commit()
    return jsonify({'status': 'review added'})

# ✅ Get all dishes
@app.route('/api/dishes', methods=['GET'])
def get_dishes():
    cursor.execute("SELECT * FROM dishes")
    return jsonify(cursor.fetchall())

if __name__ == '__main__':
    app.run(debug=True)
