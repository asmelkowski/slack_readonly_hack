import sqlite3

from flask import Flask, render_template, request, g, Response, jsonify, redirect

app = Flask(__name__)
# Load API KEY stored in .env file (not ment for git tracking)
DATABASE = 'database.db'


def get_db():
    db = getattr(g, '_database', None)
    if db is None:
        db = g._database = sqlite3.connect(DATABASE)
    return db


@app.teardown_appcontext
def close_connection(exception):
    db = getattr(g, '_database', None)
    if db is not None:
        db.close()

def create_table():
    with app.app_context():
        get_db().execute('''
            CREATE TABLE IF NOT EXISTS channels (id INTEGER PRIMARY KEY AUTOINCREMENT, 
                                                    channel TEXT,
                                                    whitelist TEXT);
            ''')

@app.route('/')
def index():
    all_data_dict = get_all_data_from_db()
    return render_template('index.html', all_data_dict=all_data_dict)


@app.route('/channels', methods=['GET', 'POST'])
def handle_data():
    if request.method == 'POST':
        try:
            with app.app_context():
                data = request.get_json()
                conn = get_db()
                conn.row_factory = sqlite3.Row
                cur = conn.cursor()
                cur.execute('''
                    INSERT INTO channels (channel, whitelist)
                    VALUES (?,?)''', (data['channel'], data['whitelist']))
                conn.commit()
                return request.get_json()
        except Exception as e:
            print(e)
    elif request.method == 'GET':
        create_table()
        all_data_dict = get_all_data_from_db()
        return jsonify(all_data_dict)

@app.route('/delete/<id>', methods=['GET'])
def delete_row(id):
    with app.app_context():
        conn = get_db()
        cur = conn.cursor()
        cur.execute('''
                    DELETE FROM channels WHERE id=? 
                    ''', (id,))
        conn.commit()
    return redirect('/')

def get_all_data_from_db():
    with app.app_context():
        create_table()
        conn = get_db()
        conn.row_factory = sqlite3.Row
        cur = conn.cursor()
        cur.execute('''
                    SELECT * FROM channels
                    ''')
        all_data = cur.fetchall()
    all_data_dict = []
    for row in all_data:
        channel = {
            'id': row['id'],
            'channel': row['channel'],
            'whitelist': row['whitelist'].split(',')
        }
        all_data_dict.append(channel)
    return all_data_dict



if __name__ == "__main__":
    app.run(host='0.0.0.0', debug=True)
