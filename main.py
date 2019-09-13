import sqlite3
import os
import sys
import requests
import multiprocessing as mp

from dotenv import load_dotenv
from deletion import run_all
from flask import Flask, render_template, request, g, Response, jsonify, redirect

app = Flask(__name__)
DATABASE = 'database.db'
process = None
os.environ["APP_STATE"] = "off"

load_dotenv()
# Load API KEY stored in .env file (not ment for git tracking)
SLACK_API_KEY = os.getenv('SLACK_API_KEY')
base_url = 'https://slack.com/api/'

# Function that initiates database
def get_db():
    with app.open_resource(DATABASE):
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
    try:
        workspace_users = requests.get(f"{base_url}users.list", params={
            'token': SLACK_API_KEY
        }).json()
        users = []
        for user in workspace_users['members']:
           if not user['deleted']:
               users.append(user)

        auth_workspaces = requests.get(f"{base_url}team.info", params={
            'token': SLACK_API_KEY
        }).json()['team']

        conversation_list = requests.get(f"{base_url}conversations.list", params={
            'token': SLACK_API_KEY,
            'limit': 999,
            'exclude_archived': True,
        }).json()['channels']

        all_data_dict = get_all_data_from_db()
        return render_template('index.html', all_data_dict=all_data_dict, workspaces=auth_workspaces, channels=conversation_list, users=users, app_state=os.environ["APP_STATE"])
    except Exception as e:
        return jsonify({
            'error': f"Exception: {e}. Check Your .env file"
        })

@app.route('/channels', methods=['GET', 'POST'])
def handle_data():
    if request.method == 'POST':
        try:
            with app.app_context():
                channel = request.form['channels']
                whitelist = ",".join([x for x in request.form.keys() if x != 'channels'])
                conn = get_db()
                conn.row_factory = sqlite3.Row
                cur = conn.cursor()
                cur.execute('''
                            SELECT * FROM channels WHERE channel = (?)
                            ''', (channel,))
                search_result = cur.fetchall()
                if search_result and whitelist != "":
                    if search_result[0]['whitelist'] == "":
                        new_whitelist = whitelist
                    else:
                        new_whitelist = search_result[0]['whitelist'] + f", {whitelist}"
                    cur.execute('''
                                UPDATE channels SET whitelist = ?
                                WHERE id = ?''', (new_whitelist, search_result[0]['id']))
                    conn.commit()
                elif search_result and whitelist == "":
                    pass
                else:
                    cur.execute('''
                        INSERT INTO channels (channel, whitelist)
                        VALUES (?,?)''', (channel, whitelist))
                    conn.commit()
                conn.close()
                return redirect('/')
        except Exception as e:
            print(e)
            return redirect("/")
    elif request.method == 'GET':
        create_table()
        all_data_dict = get_all_data_from_db()
        return jsonify(all_data_dict)

@app.route('/channels/update', methods=["POST"])
def update_channel():
    if request.method == "POST":
        try:
            row_id = request.form['id']
            row_channel = request.form['channels']
            try:
                row_whitelist = request.form['whitelist']
            except KeyError:
                row_whitelist = []
            with app.app_context():
                conn = get_db()
                conn.row_factory = sqlite3.Row
                cur = conn.cursor()
                cur.execute('''
                            UPDATE channels SET whitelist = ?
                            WHERE id = ?''', (row_whitelist, row_id))
                conn.commit()
                conn.close()
        except Exception as e:
            print(e)
    return redirect("/")

@app.route('/delete/<id>', methods=['GET'])
def delete_row(id):
    with app.app_context():
        conn = get_db()
        cur = conn.cursor()
        cur.execute('''
                    DELETE FROM channels WHERE id=? 
                    ''', (id,))
        conn.commit()
        conn.close()
    return redirect('/')
    
# Route ment for running and stopping deletion.py
@app.route('/state', methods=['GET', 'POST'])
def run_slack_app():
    if request.method == 'POST':
        data = request.form['set_state']
        if data == 'on':
            try:
                global process
                process = mp.Process(target=run_all)
                process.start()
            except Exception as e:
                print(e)
            finally:
                os.environ['APP_STATE'] = 'on'
        elif data == 'off':
            try:
                process.terminate()
            except Exception as e:
                print(e)
            finally:
                os.environ['APP_STATE'] = 'off'
        return redirect("/")
    return jsonify({'current_state': os.environ['APP_STATE']})


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
        all_data_dict.append({
            'id': row['id'],
            'channel': row['channel'],
            'whitelist': row['whitelist'].split(',')
        })
    return all_data_dict


if __name__ == "__main__":
    app.run(host='0.0.0.0', debug=True)
