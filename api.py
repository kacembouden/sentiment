from flask import Flask, jsonify, request, render_template
import sqlite3
import re

app = Flask(__name__)

# Create a connection to the SQLite database
conn = sqlite3.connect('items.db' ,check_same_thread=False)
cursor = conn.cursor()

# Create the items table if it doesn't exist
cursor.execute('''
                   CREATE TABLE IF NOT EXISTS items
                  (id INTEGER PRIMARY KEY AUTOINCREMENT,
                  name TEXT,
                  value_daily INTEGER ,
                  value_weekly,
                  value_monthly,
                  value_over_all)''')
conn.commit()

# Endpoint to get all items
@app.route('/items', methods=['GET'])
def get_items():
    cursor.execute("SELECT * FROM items")
    items = [{'id': row[0], 'name': row[1]} for row in cursor.fetchall()]
    return jsonify(items)

# Endpoint to get a specific item by ID
@app.route('/items/<int:item_id>', methods=['GET'])
def get_item(item_id):
    cursor.execute("SELECT * FROM items WHERE id=?", (item_id,))
    item = cursor.fetchone()
    if item:
        return jsonify({'id': item[0], 'name': item[1]})
    return jsonify({'message': 'Item not found'}), 404

# Endpoint to create a new item
@app.route('/items', methods=['POST'])
def create_item():
    name = request.json['name']
    cursor.execute("INSERT INTO items (name) VALUES (?)", (name,))
    conn.commit()
    item_id = cursor.lastrowid
    return jsonify({'id': item_id, 'name': name}), 201

# Endpoint to update an existing item
@app.route('/items/<int:item_id>', methods=['PUT'])
def update_item(item_id):
    name = request.json['name']
    cursor.execute("UPDATE items SET name=? WHERE id=?", (name, item_id))
    conn.commit()
    if cursor.rowcount > 0:
        return jsonify({'id': item_id, 'name': name})
    return jsonify({'message': 'Item not found'}), 404

# Endpoint to delete an item
@app.route('/items/<int:item_id>', methods=['DELETE'])
def delete_item(item_id):
    cursor.execute("DELETE FROM items WHERE id=?", (item_id,))
    conn.commit()
    if cursor.rowcount > 0:
        return jsonify({'message': 'Item deleted'})
    return jsonify({'message': 'Item not found'}), 404




############################## Users ################################


conn = sqlite3.connect('users.db')
cursor = conn.cursor()

# Create the users table if it doesn't exist
cursor.execute('''CREATE TABLE IF NOT EXISTS users
                  (id INTEGER PRIMARY KEY AUTOINCREMENT,
                  first_name TEXT,
                  last_name TEXT,
                  email TEXT,
                  location TEXT,
                  age INTEGER,
                  premium INTEGER)''')
conn.commit()

# Validate email format
def is_valid_email(email):
    email_regex = r'^[\w\.-]+@[\w\.-]+\.\w+$'
    return re.match(email_regex, email) is not None

# Validate name format (characters only)
def is_valid_name(name):
    name_regex = r'^[a-zA-Z\s]+$'
    return re.match(name_regex, name) is not None

# Endpoint to get all users
@app.route('/users', methods=['GET'])
def get_users():
    cursor.execute("SELECT * FROM users")
    users = [{'id': row[0], 'first_name': row[1], 'last_name': row[2], 'email': row[3], 'location': row[4], 'age': row[5], 'premium': bool(row[6])} for row in cursor.fetchall()]
    return jsonify(users)

# Endpoint to get a specific user by ID
@app.route('/users/<int:user_id>', methods=['GET'])
def get_user(user_id):
    cursor.execute("SELECT * FROM users WHERE id=?", (user_id,))
    user = cursor.fetchone()
    if user:
        return jsonify({'id': user[0], 'first_name': user[1], 'last_name': user[2], 'email': user[3], 'location': user[4], 'age': user[5], 'premium': bool(user[6])})
    return jsonify({'message': 'User not found'}), 404

# Endpoint to create a new user
@app.route('/users', methods=['POST'])
def create_user():
    first_name = request.json['first_name']
    last_name = request.json['last_name']
    email = request.json['email']
    location = request.json['location']
    age = request.json['age']
    premium = request.json['premium']

    # Validate name format
    if not is_valid_name(first_name) or not is_valid_name(last_name):
        return jsonify({'message': 'Invalid name format'}), 400

    # Validate email format
    if not is_valid_email(email):
        return jsonify({'message': 'Invalid email format'}), 400

    # Validate age as an integer
    try:
        age = int(age)
    except ValueError:
        return jsonify({'message': 'Invalid age format'}), 400

    cursor.execute("INSERT INTO users (first_name, last_name, email, location, age, premium) VALUES (?, ?, ?, ?, ?, ?)",
                   (first_name, last_name, email, location, age, premium))
    conn.commit()
    user_id = cursor.lastrowid
    return jsonify({'id': user_id, 'first_name': first_name, 'last_name': last_name, 'email': email, 'location': location, 'age': age, 'premium': premium}), 201





# Close the connection when the application is terminated
@app.teardown_appcontext
def close_connection(exception):
    conn.close()

# Run the application
if __name__ == '__main__':
    app.run(debug=True)
