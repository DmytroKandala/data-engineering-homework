import requests
import sqlite3
import os
import time

DB_PATH = "/app/taxi.db"
API_URL = "https://my-taxi-pipeline-bd9f765ed57d.herokuapp.com/rides"

def get_rides():
    response = requests.get(API_URL)
    return response.json()

def update_driver_stats(rides):
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()

    cursor.execute("""
        CREATE TABLE IF NOT EXISTS driver_statistics (
            driver_id TEXT PRIMARY KEY,
            total_distance REAL
        )
    """)

    stats = {}
    for ride in rides:
        stats[ride["driver_id"]] = stats.get(ride["driver_id"], 0) + ride["distance"]

    for driver_id, total_distance in stats.items():
        cursor.execute("""
            INSERT INTO driver_statistics (driver_id, total_distance)
            VALUES (?, ?)
            ON CONFLICT(driver_id) DO UPDATE SET total_distance = total_distance + ?
        """, (driver_id, total_distance, total_distance))

    conn.commit()
    conn.close()

if __name__ == "__main__":
    print("Waiting for API to be available...")
    time.sleep(3)  # даем API подняться
    rides = get_rides()
    update_driver_stats(rides)
