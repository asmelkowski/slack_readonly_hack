import sqlite3
import subprocess
import os
import requests

from dotenv import load_dotenv
from flask import Flask, render_template, request, g, Response, jsonify, redirect

app = Flask(__name__)
# Load API KEY stored in .env file (not ment for git tracking)
DATABASE = 'database.db'
process = None
state = None

load_dotenv()
# Load API KEY stored in .env file (not ment for git tracking)
SLACK_API_KEY = os.getenv('SLACK_API_KEY')
base_url = 'https://slack.com/api/'

# Function that initiates database


def get_db():
    db = getattr(g, '_database', None)
    if db is None:
        db = g._database = sqlite3.connect(DATABASE)
    return db

# Closes db connection when context is done
@app.teardown_appcontext
def close_connection(exception):
    db = getattr(g, '_database', None)
    if db is not None:
        db.close()
# Creates table "channels" if it doesn't exists


def create_table():
    with app.app_context():
        get_db().execute('''
            CREATE TABLE IF NOT EXISTS channels (id INTEGER PRIMARY KEY AUTOINCREMENT, 
                                                    channel TEXT,
                                                    whitelist TEXT);
            ''')


@app.route('/')
def index():
    workspace_users = requests.get(f"{base_url}users.list", params={
        'token': SLACK_API_KEY
    }).json()
    users_name_list = [x['real_name'] for x in workspace_users['members']]
    users_id_list = [x['id'] for x in workspace_users['members']]
    workspace_users = zip(users_id_list, users_name_list)
    auth_workspaces = requests.get(f"{base_url}team.info", params={
        'token': SLACK_API_KEY
    }).json()
    if type(auth_workspaces['team']) == dict:
        workspaces_ids = [auth_workspaces['team']['id']]
        workspaces_names = [auth_workspaces['team']['name']]
        workspaces_domains = [auth_workspaces['team']['domain']]
        auth_workspaces = zip(workspaces_ids, workspaces_names, workspaces_domains)
    elif type(auth_workspaces['team']) == list:
        workspaces_ids = [x['id'] for x in auth_workspaces['team']]
        workspaces_names = [x['name'] for x in auth_workspaces['team']]
        workspaces_domains = [x['domain'] for x in auth_workspaces['team']]
        auth_workspaces = zip(workspaces_ids, workspaces_names, workspaces_domains)

    conversation_list = requests.get(f"{base_url}conversations.list", params={
        'token': SLACK_API_KEY
    }).json()
    channels_ids = [x['id'] for x in conversation_list['channels']]
    channels_names = [x['name'] for x in conversation_list['channels']]
    conversation_list = zip(channels_ids, channels_names)
    all_data_dict = get_all_data_from_db()
    return render_template('index.html', all_data_dict=all_data_dict, workspaces=auth_workspaces, conversations=conversation_list, users=workspace_users)


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
# Route ment for running and stopping deletion.py
@app.route('/state', methods=['GET', 'POST'])
def run_slack_app():
    if request.method == 'POST':
        data = request.get_json()
        if data['set_state'] == 'on':
            global process
            process = subprocess.Popen('py deletion.py')
            global state
            state = "on"
            print(state)
        elif data['set_state'] == 'off':
            try:
                process.kill()
                state = "off"
                print(state)
            except NameError as e:
                print(e)
                print("Proccess was not running")
    return jsonify({'current_state': state})


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
