import sqlite3

def get_db():
    con = sqlite3.connect("money.db")
    con.row_factory = sqlite3.Row
    return con

def init_db():
    con = get_db()
    cur = con.cursor()

    cur.execute(
        "CREATE TABLE IF NOT EXISTS transactions (id INTEGER PRIMARY KEY AUTOINCREMENT, type TEXT, category TEXT, note TEXT, amount REAL, date TEXT)"
    )

    con.commit()
    con.close()
