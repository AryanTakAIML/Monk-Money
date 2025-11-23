from flask import Flask, render_template, request, jsonify
from db import init_db, get_db

app = Flask(__name__)

# main homepage
@app.route("/")
def index():
    return render_template("index.html")


# add new transaction
@app.route("/add", methods=["POST"])
def add():
    data = request.json

    conn = get_db()
    cur = conn.cursor()

    # inserting into db
    cur.execute(
        "INSERT INTO transactions (type, category, note, amount, date) VALUES (?, ?, ?, ?, ?)",
        (
            data["type"],
            data["category"],
            data.get("note", ""),
            data["amount"],
            data["date"]
        )
    )

    conn.commit()
    conn.close()

    return jsonify({"ok": True})


# get all transactions
@app.route("/all")
def all_data():
    conn = get_db()
    cur = conn.cursor()

    cur.execute("SELECT * FROM transactions ORDER BY date DESC")
    rows = cur.fetchall()

    out = []
    for r in rows:
        out.append(dict(r))

    conn.close()
    return jsonify(out)


# initialize database table
init_db()

# running server
if __name__ == "__main__":
    app.run(debug=True)
