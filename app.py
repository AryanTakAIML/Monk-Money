from flask import Flask, render_template, request, jsonify
from db import init_db, get_db

app = Flask(__name__)

# ------------------ ROUTES ------------------ #

@app.route('/')
def home():
    return render_template('index.html')

@app.route('/add', methods=['POST'])
def add_transaction():
    data = request.json
    conn = get_db()
    cursor = conn.cursor()

    cursor.execute("""
        INSERT INTO transactions (type, category, note, amount, date)
        VALUES (?, ?, ?, ?, ?)
    """, (
        data['type'],
        data['category'],
        data.get('note', ''),
        data['amount'],
        data['date']
    ))

    conn.commit()
    conn.close()

    return jsonify({"status": "success"})

@app.route('/all')
def get_all():
    conn = get_db()
    cursor = conn.cursor()

    cursor.execute("SELECT * FROM transactions ORDER BY date DESC")
    rows = cursor.fetchall()

    data = [dict(row) for row in rows]

    conn.close()
    return jsonify(data)

# ------------------ INITIALIZE DB ------------------ #

init_db()

# ------------------ RUN SERVER ------------------ #
if __name__ == '__main__':
    app.run(debug=True)
