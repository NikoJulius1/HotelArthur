import sqlite3

# Connect to the SQLite database (or create it if it doesn't exist)
conn = sqlite3.connect('reservation_database.db')
cursor = conn.cursor()

# Create the  table if it doesn't already exist
cursor.execute('''
    CREATE TABLE IF NOT EXISTS booking (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        roomnumber INTEGER NOT NULL, 
        category TEXT CHECK(category IN (
            'Standard single room', 
            'Grand lit room', 
            'Standard dobbeltroom', 
            'Superior room', 
            'Junior suite', 
            'Spa executive room', 
            'Suite room', 
            'Loft room'
        )),
        isbooking INTEGER CHECK(isbooking IN (0, 1)),  -- 0 for False, 1 for True,
        is_cleaned INTEGER DEFAULT 0 CHECK(is_cleaned IN (0, 1)),  -- 0 for not cleaned, 1 for cleaned,
        checkin DATETIME,
        checkout DATETIME
    )
''')

# Function to insert a new booking
def insert_booking(roomnumber, category, isbooking, checkin, checkout):
    valid_categories = [
        'Standard single room', 
        'Grand lit room', 
        'Standard dobbeltroom', 
        'Superior room', 
        'Junior suite', 
        'Spa executive room', 
        'Suite room', 
        'Loft room'
    ]
    if category not in valid_categories:
        print(f"Error: '{category}' is not a valid category.")
        return
    
    cursor.execute('''
        INSERT INTO booking (roomnumber, category, isbooking, checkin, checkout)
        VALUES (?, ?, ?, ?, ?)
    ''', (roomnumber, category, isbooking, checkin, checkout))
    conn.commit()

insert_booking(101, 'Standard single room', 1, '2024-11-01 14:00:00', '2024-11-05 12:00:00')


# Close the database connection
conn.close()