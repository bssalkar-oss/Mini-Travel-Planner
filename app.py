import os
import json
from flask import Flask, render_template, request, redirect, url_for, flash

app = Flask(__name__)
app.secret_key = os.environ.get("FLASK_SECRET_KEY") or os.urandom(32)

DATA_DIR = "data"
DATA_FILE = os.path.join(DATA_DIR, "trips.json")

def ensure_data_file():
    """Ensure the data directory and JSON file exist."""
    if not os.path.exists(DATA_DIR):
        os.makedirs(DATA_DIR)
    if not os.path.exists(DATA_FILE):
        with open(DATA_FILE, "w") as f:
            json.dump([], f)

def load_trips():
    """Load trip records from JSON file with error handling."""
    ensure_data_file()
    try:
        with open(DATA_FILE, "r") as f:
            return json.load(f)
    except (json.JSONDecodeError, IOError):
        return []

def save_trips(trips):
    """Save trip records to JSON file."""
    ensure_data_file()
    with open(DATA_FILE, "w") as f:
        json.dump(trips, f, indent=4)

@app.route("/")
def index():
    """Feature 2 & 3: View all trips, search by destination, and show summary totals."""
    search_query = request.args.get("search", "").strip().lower()
    trips = load_trips()
    # Filter trips if search query is provided
    if search_query:
        filtered_trips = [t for t in trips if search_query in t["destination"].lower()]
    else:
        filtered_trips = trips

    # Calculate total estimated budget across all trips
    total_budget = sum(float(t["budget"]) for t in trips)

    return render_template(
        "index.html",
        trips=filtered_trips,
        total_budget=total_budget,
        search_query=search_query
    )

@app.route("/add", methods=["POST"])
def add_trip():
    """Feature 1: Add new trip with input validation."""
    destination = request.form.get("destination", "").strip()
    start_date = request.form.get("start_date", "").strip()
    end_date = request.form.get("end_date", "").strip()
    budget_str = request.form.get("budget", "").strip()

    # Validation Rule 1: Check for blank fields
    if not destination or not start_date or not end_date or not budget_str:
        flash("All fields are required and cannot be blank.", "error")
        return redirect(url_for("index"))

    # Validation Rule 2: Validate positive numeric budget
    try:
        budget = float(budget_str)
        if budget <= 0:
            raise ValueError("Budget must be greater than zero.")
    except ValueError:
        flash("Invalid budget entered. Please enter a positive number.", "error")
        return redirect(url_for("index"))

    trips = load_trips()
    new_id = max([t.get("id", 0) for t in trips], default=0) + 1

    new_trip = {
        "id": new_id,
        "destination": destination,
        "start_date": start_date,
        "end_date": end_date,
        "budget": round(budget, 2)
    }

    trips.append(new_trip)
    save_trips(trips)
    flash("Trip destination successfully added!", "success")
    return redirect(url_for("index"))

@app.route("/delete/<int:trip_id>", methods=["POST"])
def delete_trip(trip_id):
    """Feature 4: Delete an existing trip record."""
    trips = load_trips()
    updated_trips = [t for t in trips if t["id"] != trip_id]

    if len(updated_trips) == len(trips):
        flash("Trip record not found.", "error")
    else:
        save_trips(updated_trips)
        flash("Trip deleted successfully.", "success")

    return redirect(url_for("index"))

if __name__ == "__main__":
    ensure_data_file()
    app.run(debug=True, port=5000)