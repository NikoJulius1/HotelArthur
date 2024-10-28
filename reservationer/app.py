
import sqlite3
from flask import Flask, request, jsonify

app = Flask(__name__)

#Connect til databasen
conn = sqlite3.connect('reservation_database.db')
cursor = conn.cursor()

@app.route('/bookings', methods=['GET'])
def isAvailable(roomnumber, checkin, checkout):
    cursor.execute('''
                   SELECT * FROM booking
                   WHERE roomnumber = ?
                   AND checkin < ?
                   AND checkout > ?
                   ''', (roomnumber, checkout, checkin))
    overlapping_bookings = cursor.fetchall()
    if overlapping_bookings:
        return False  # Room is not available
    else:
        return True   # Room is available
    
@app.route('/bookings/<int:booking_id>', methods=['PUT'])    
def makeBooking(roomnumber, category, checkin, checkout):
    if isAvailable(roomnumber, checkin, checkout):

        print(f"Inserting: {roomnumber}, {category}, {checkin}, {checkout}")


        cursor.execute('''
            INSERT INTO booking (roomnumber, category, isbooking, checkin, checkout)
            VALUES (?, ?, ?, ?, ?)
                       ''', (roomnumber, category, 1, checkin, checkout))
        
        # Gem ændringerne i databasen
        conn.commit()

        return "Værelse reserveret"
    else:
        return "Værelse ikk tilgængelig"


roomnumber = 101
category = 'Standard single room'
checkin = '2024-11-01 14:00:00'
checkout = '2024-11-05 11:00:00'

# Call makeBooking to attempt a reservation
result = makeBooking(roomnumber, category, checkin, checkout)
print(result)  # Should print "Værelse reserveret" or "Værelse ikke tilgængelig"

# Fetch all rows to verify the insertion
cursor.execute("SELECT * FROM booking")
results = cursor.fetchall()
print(results)  # Should display all bookings in the table, including the new one

result = makeBooking(roomnumber, category, checkin, checkout)
print(result)  # Should print "Værelse reserveret" or "Værelse ikke tilgængelig"

# Close the connection (good practice)
conn.close()