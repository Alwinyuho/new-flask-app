from flask import Flask, render_template
import os
import psycopg2

app = Flask(_name_)

DATABASE_URL = os.environ['DATABASE_URL']

def get_db_connection():
    conn = psycopg2.connect(DATABASE_URL, sslmode='require')
    return conn

@app.route('/')
def index():
    conn = get_db_connection()
    cur = conn.cursor()
    cur.execute('SELECT * FROM my_table;')
    results = cur.fetchall()
    cur.close()
    conn.close()
    return render_template('index.html', results=results)

if _name_ == '_main_':
    app.run(debug=True, host='0.0.0.0')
