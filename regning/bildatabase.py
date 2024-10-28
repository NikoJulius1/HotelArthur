import sqlite3
from datetime import datetime

conn_booking = sqlite3.connect('reservation_database.db')
conn_billing = sqlite3.connect('billing_database.db')

cursor_booking = conn_booking.cursor()
cursor_billing = conn_billing.cursor()

# Create billing table with season column
cursor_billing.execute(''' 
    CREATE TABLE IF NOT EXISTS billing (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        booking_id INTEGER,
        room_type TEXT,
        days_stayed INTEGER,
        season TEXT,
        daily_rate REAL, 
        total_bill REAL, 
        FOREIGN KEY (booking_id) REFERENCES booking(id) 
    ) 
''')

room_rates = {
    'Standard single room': {'high': 1200, 'mid': 1050, 'low': 900},
    'Grand lit room': {'high': 1400, 'mid': 1250, 'low': 1100},
    'Standard dobbeltroom': {'high': 1600, 'mid': 1400, 'low': 1200},
    'Superior room': {'high': 2000, 'mid': 1700, 'low': 1400},
    'Junior suite': {'high': 2500, 'mid': 2150, 'low': 1800},
    'Spa executive room': {'high': 2800, 'mid': 2400, 'low': 2000},
    'Suite room': {'high': 3500, 'mid': 3000, 'low': 2500},
    'Loft room': {'high': 4000, 'mid': 3500, 'low': 3000},
}

def determine_season(checkin_date):
    if checkin_date.month in [6, 7, 8, 12]:
        return 'high'
    if checkin_date.month in [4, 5, 9, 10]:
        return 'mid'
    else:
        return 'low'

def generate_bill(booking_id):
    cursor_booking.execute('SELECT category, checkin, checkout FROM booking WHERE id = ?', (booking_id,))
    booking = cursor_booking.fetchone()

    if booking:
        room_type, checkin, checkout = booking
        checkin_date = datetime.strptime(checkin, '%Y-%m-%d %H:%M:%S')
        checkout_date = datetime.strptime(checkout, '%Y-%m-%d %H:%M:%S')
        
        # Calculate days stayed
        days_stayed = (checkout_date - checkin_date).days
        
        # Determine season and rate
        season = determine_season(checkin_date)
        daily_rate = room_rates[room_type][season]
        total_bill = days_stayed * daily_rate
        
        # Insert into billing table
        cursor_billing.execute('''
            INSERT INTO billing (booking_id, room_type, days_stayed, season, daily_rate, total_bill)
            VALUES (?, ?, ?, ?, ?, ?)
        ''', (booking_id, room_type, days_stayed, season, daily_rate, total_bill))
        conn_billing.commit()

# Example usage of generate_bill function
generate_bill(1)

conn_booking.close()
conn_billing.close()
