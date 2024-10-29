import sqlite3 
from flask import Flask, request, jsonift
import requests


app = Flask(__name__)


# Fetch and print room bookings
bookings = requests.get("http://localhost:5000/bookings").json()

print("Rooms that need cleaning or preparation:")
for booking in bookings:
    print("Room:", booking[1], "| Check-In:", booking[4], "| Check-Out:", booking[5])


