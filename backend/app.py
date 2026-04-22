from flask import Flask, request, jsonify
import psycopg2
import os

app = Flask(__name__)

DATABASE_URL = os.environ.get("DATABASE_URL")

def get_conn():
    return psycopg2.connect(DATABASE_URL)

@app.route('/api/data', methods=['GET'])
def get_data():
    conn = get_conn()
    cur = conn.cursor()
    cur.execute("SELECT id, name FROM items;")
    rows = cur.fetchall()
    cur.close()
    conn.close()
    return jsonify(rows)

@app.route('/api/data', methods=['POST'])
def add_data():
    data = request.json
    conn = get_conn()
    cur = conn.cursor()
    cur.execute("INSERT INTO items (name) VALUES (%s);", (data['name'],))
    conn.commit()
    cur.close()
    conn.close()
    return jsonify({"status": "added"})

@app.route('/api/data/<int:id>', methods=['DELETE'])
def delete_data(id):
    conn = get_conn()
    cur = conn.cursor()
    cur.execute("DELETE FROM items WHERE id=%s;", (id,))
    conn.commit()
    cur.close()
    conn.close()
    return jsonify({"status": "deleted"})

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 10000))
    app.run(host="0.0.0.0", port=port)
