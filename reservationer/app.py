import sqlite3
from flask import Flask, request, jsonify, Response

app = Flask(__name__)

# Connect to the SQLite database
def get_db_connection():
    return sqlite3.connect('reservation_database.db')

def notify_billing_service(booking_id):
    try:
        billing_url = f'http://billing-service:5000/bills/update/{booking_id}'
        response = request.post(billing_url)
        if response.status_code == 200:
            print(f"Billing updated for booking {booking_id}")
        else:
            print(f"Failed to update billing for booking {booking_id}: {response.json()}")
    except Exception as e:
        print(f"Error contacting billing service: {e}")

# Check room availability
def isAvailable(roomnumber, checkin, checkout):
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute('''
        SELECT * FROM booking
        WHERE roomnumber = ?
        AND checkin < ?
        AND checkout > ?
    ''', (roomnumber, checkout, checkin))
    overlapping_bookings = cursor.fetchall()
    conn.close()
    return len(overlapping_bookings) == 0

# List all bookings
@app.route('/bookings', methods=['GET'])
def list_bookings():
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute('SELECT * FROM booking')
    bookings = cursor.fetchall()
    conn.close()
    return jsonify(bookings)

# Create a new booking
@app.route('/bookings', methods=['POST'])
def create_booking():
    data = request.get_json()
    roomnumber = data['roomnumber']
    category = data['category']
    checkin = data['checkin']
    checkout = data['checkout']

    if isAvailable(roomnumber, checkin, checkout):
        conn = get_db_connection()
        cursor = conn.cursor()
        cursor.execute('''
            INSERT INTO booking (roomnumber, category, isbooking, checkin, checkout)
            VALUES (?, ?, 1, ?, ?)
        ''', (roomnumber, category, checkin, checkout))
        conn.commit()
        booking_id = cursor.lastrowid
        conn.close()
        notify_billing_service(booking_id)
        return jsonify({"message": "Booking created successfully"}), 201
    else:
        return jsonify({"message": "Room not available"}), 409
    
# Mark booking as done
@app.route('/bookings/<int:booking_id>/mark_done', methods=['PUT'])
def mark_booking_done(booking_id):
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute('''
        UPDATE booking 
        SET is_cleaned = 1 
        WHERE id = ?
    ''', (booking_id,))
    conn.commit()
    conn.close()
    return jsonify({"message": "Booking marked as done"}), 200


# Export bookings in CSV format
@app.route('/bookings/export/csv', methods=['GET'])
def export_bookings_csv():
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute('SELECT * FROM booking')
    rows = cursor.fetchall()
    conn.close()

    # Convert rows to CSV format
    csv_data = "id,roomnumber,category,isbooking,checkin,checkout\n"
    for row in rows:
        csv_data += ",".join(str(item) for item in row) + "\n"

    return Response(csv_data, mimetype='text/csv',
                    headers={"Content-Disposition": "attachment;filename=bookings.csv"})

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5001)
