from flask import Flask, jsonify

app = Flask(__name__)

@app.route("/rides", methods=["GET"])
def get_rides():
    return jsonify([
        {"ride_id": 1, "driver_id": "d_001", "distance": 12.4},
        {"ride_id": 2, "driver_id": "d_001", "distance": 6.5},
        {"ride_id": 3, "driver_id": "d_002", "distance": 15.7}
    ])

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)
