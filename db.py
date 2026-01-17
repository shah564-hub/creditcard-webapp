import sqlite3


DB_NAME = "credit_card_app.db"


def get_conn():
    return sqlite3.connect(DB_NAME, check_same_thread=False)


def init_db():
    conn = get_conn()
    cur = conn.cursor()

    cur.execute("""
    CREATE TABLE IF NOT EXISTS customers (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        name TEXT NOT NULL,
        email TEXT NOT NULL
    )
    """)

    cur.execute("""
    CREATE TABLE IF NOT EXISTS cards (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        customer_id INTEGER NOT NULL,
        last4 TEXT NOT NULL,
        brand TEXT NOT NULL,
        expiry TEXT NOT NULL,
        FOREIGN KEY(customer_id) REFERENCES customers(id)
    )
    """)

    cur.execute("""
    CREATE TABLE IF NOT EXISTS transactions (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        customer_id INTEGER NOT NULL,
        amount REAL NOT NULL,
        status TEXT NOT NULL,
        message TEXT NOT NULL,
        time TEXT NOT NULL,
        FOREIGN KEY(customer_id) REFERENCES customers(id)
    )
    """)

    conn.commit()
    conn.close()


def add_customer(name, email):
    conn = get_conn()
    cur = conn.cursor()
    cur.execute("INSERT INTO customers (name, email) VALUES (?, ?)", (name, email))
    conn.commit()
    conn.close()


def get_customers():
    conn = get_conn()
    cur = conn.cursor()
    cur.execute("SELECT id, name, email FROM customers ORDER BY id DESC")
    rows = cur.fetchall()
    conn.close()
    return rows


def delete_customer(customer_id):
    conn = get_conn()
    cur = conn.cursor()
    cur.execute("DELETE FROM cards WHERE customer_id=?", (customer_id,))
    cur.execute("DELETE FROM transactions WHERE customer_id=?", (customer_id,))
    cur.execute("DELETE FROM customers WHERE id=?", (customer_id,))
    conn.commit()
    conn.close()


def add_card(customer_id, last4, brand, expiry):
    conn = get_conn()
    cur = conn.cursor()
    cur.execute(
        "INSERT INTO cards (customer_id, last4, brand, expiry) VALUES (?, ?, ?, ?)",
        (customer_id, last4, brand, expiry),
    )
    conn.commit()
    conn.close()


def get_cards(customer_id):
    conn = get_conn()
    cur = conn.cursor()
    cur.execute(
        "SELECT id, last4, brand, expiry FROM cards WHERE customer_id=? ORDER BY id DESC",
        (customer_id,),
    )
    rows = cur.fetchall()
    conn.close()
    return rows


def delete_card(card_id):
    conn = get_conn()
    cur = conn.cursor()
    cur.execute("DELETE FROM cards WHERE id=?", (card_id,))
    conn.commit()
    conn.close()


def add_transaction(customer_id, amount, status, message, time):
    conn = get_conn()
    cur = conn.cursor()
    cur.execute(
        "INSERT INTO transactions (customer_id, amount, status, message, time) VALUES (?, ?, ?, ?, ?)",
        (customer_id, amount, status, message, time),
    )
    conn.commit()
    conn.close()


def get_transactions(customer_id):
    conn = get_conn()
    cur = conn.cursor()
    cur.execute(
        "SELECT id, amount, status, message, time FROM transactions WHERE customer_id=? ORDER BY id DESC",
        (customer_id,),
    )
    rows = cur.fetchall()
    conn.close()
    return rows
