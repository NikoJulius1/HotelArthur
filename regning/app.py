import sqlite3 
from flask import Flask, request, jsonify 


app = Flask(__name__) 

#Forbindelse til database for at få adgang til regning database:  
def get_db_connection():
    conn = sqlite3.connect('billing_database.db')
    conn.row_factory = sqlite3.Row  
    return conn

#Giver adgang til regninger i hele databasen 
@app.route('/bils', methods=['GET'])
def get_all_bills():
    db = get_db_connection()
    cursor = db.cursor()
    cursor.execute('SELECT * FROM billing')
    bills = cursor.fetchall()
    db.close()
    return jsonify([dict(row) for row in bills])

#Giver adgang til specifik regning databasen via: id
@app.route('/bils/<int:id>', methods=['GET'])
def get_bil_by_id(id):
    db = get_db_connection()
    cursor = db.cursor()
    cursor.execute('SELECT * FROM billing where id =?',(id,))
    bill = cursor.fetchall()
    db.close()
    if bill is None:
        return jsonify({'error': 'Bill not found'}), 404
    
    return jsonify([dict(row) for row in bill])



if __name__ == '__main__':
    app.run(debug=True) 