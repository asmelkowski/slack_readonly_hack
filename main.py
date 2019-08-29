import os
import sqlite3
import time
import requests
import json

from dotenv import load_dotenv
from flask import Flask, render_template, request, g, Response, jsonify

app = Flask(__name__)
load_dotenv()
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


with app.app_context():
    get_db().execute('''
        CREATE TABLE IF NOT EXISTS channels (id INTEGER PRIMARY KEY AUTOINCREMENT, 
                                                channel TEXT,
                                                whitelist TEXT);
        ''')
SLACK_API_KEY = os.getenv('SLACK_API_KEY')
base_url = 'https://slack.com/api/'


@app.route('/')
def index():
    return render_template('index.html')


@app.route('/channels', methods=['GET', 'POST'])
def handle_data():
    if request.method == 'POST':
        try:
            data = request.get_json()
            print(
                f"Channel is: {data['channel']}, Whitelist is: {data['whitelist']}")
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
        return jsonify(all_data_dict)


def delete_messages(channel_list, whitelisted_users):
    for channel in channel_list:
        messages_history = requests.get(f"{base_url}conversations.history", params={
            'token': SLACK_API_KEY,
            'channel': channel
        })
        for message in messages_history.json()['messages']:
            try:
                if message['user'] not in whitelisted_users:
                    delete_request = requests.post(f"{base_url}chat.delete", data={
                        'token': SLACK_API_KEY,
                        'channel': channel,
                        'ts': message['ts']
                    })
            except KeyError:
                print(f"No user was found in message {message['ts']}")

# while True:
#     delete_messages(['CMSN6JXL4'], whitelisted_users)
#     time.sleep(5)


if __name__ == "__main__":
    app.run(host='0.0.0.0', debug=True)
