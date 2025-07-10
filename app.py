from flask import Flask, request, jsonify, send_from_directory
from flask_cors import CORS
import mysql.connector
import os
from flask import Flask, request, jsonify
from appwrite.client import Client
from appwrite.services.databases import Databases
from appwrite.exception import AppwriteException
from dotenv import load_dotenv

load_dotenv()

app = Flask(__name__)

# Initialize Appwrite client
client = Client()

client.set_endpoint(os.environ.get('APPWRITE_PROJECT_ID'))  # or your self-hosted URL
client.set_project(os.environ.get("APPWRITE_ENDPOINT"))  # Replace with your project ID
client.set_key(os.environ.get("APPWRITE_KEY"))  # Use an API key with database access

# Initialize the Databases service
database = Databases(client, database_id=os.environ.get('DATABASE_ID'))


app = Flask(__name__, static_folder=".", static_url_path="")
CORS(app)

# MySQL connection
db = mysql.connector.connect(
    host=os.environ.get("DB_HOST", "localhost"),
    user=os.environ.get("DB_USER", "root"),
    password=os.environ.get("DB_PASSWORD", "unsu@123"),
    database=os.environ.get("DB_NAME", "tastescape")
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
    try:
        # Fetch all reviews
        reviews_data = database.list_documents(
            collection_id=os.environ.get("REVIEWS_COLLECTION_ID")
        )['documents']

        # Fetch all restaurants (so we can map their IDs to names)
        restaurants_data = database.list_documents(
            collection_id=os.environ.get("RESTAURANTS_COLLECTION_ID")
        )['documents']

        # Create a mapping: restaurant_id -> restaurant name
        restaurant_map = {res['$id']: res['name'] for res in restaurants_data}

        # Build response
        result = []
        for review in reviews_data:
            result.append({
                "user": review.get("user"),
                "rating": review.get("rating"),
                "comment": review.get("comment"),
                "restaurant": restaurant_map.get(review.get("restaurant_id"), "Unknown")
            })

        return jsonify(result)

    except AppwriteException as e:
        return jsonify({"error": str(e)}), 500

# --- Run the app on the correct port (for Render) ---
if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5000))
    app.run(host="0.0.0.0", port=port)
