from flask import Flask, request, jsonify
import sqlite3

app = Flask(__name__)

def get_db_connection():
    conn = sqlite3.connect('products.db')
    conn.row_factory = sqlite3.Row
    return conn

@app.route('/health', methods=['GET'])
def health_check():
    return jsonify({"status": "up"}), 200

@app.route('/products', methods=['GET'])
def get_products():
    conn = get_db_connection()
    products = conn.execute('SELECT * FROM products').fetchall()
    conn.close()
    return jsonify([dict(row) for row in products])

@app.route('/products', methods=['POST'])
def create_product():
    new_product = request.get_json()
    conn = get_db_connection()
    conn.execute('INSERT INTO products (name, price, description) VALUES (?, ?, ?)',
                 (new_product['name'], new_product['price'], new_product['description']))
    conn.commit()
    conn.close()
    return jsonify(new_product), 201

@app.route('/products/<int:id>', methods=['PUT'])
def update_product(id):
    updated_product = request.get_json()
    conn = get_db_connection()
    conn.execute('UPDATE products SET name = ?, price = ?, description = ? WHERE id = ?',
                 (updated_product['name'], updated_product['price'], updated_product['description'], id))
    conn.commit()
    conn.close()
    return jsonify(updated_product)

@app.route('/products/<int:id>', methods=['DELETE'])
def delete_product(id):
    conn = get_db_connection()
    conn.execute('DELETE FROM products WHERE id = ?', (id,))
    conn.commit()
    conn.close()
    return '', 204

if __name__ == '__main__':
    app.run(debug=True)
