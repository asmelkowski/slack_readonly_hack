import requests
import sqlite3
import os
import time
from dotenv import load_dotenv

load_dotenv()
# Load API KEY stored in .env file (not ment for git tracking)
SLACK_API_KEY = os.getenv('SLACK_API_KEY')
base_url = 'https://slack.com/api/'
DATABASE = 'database.db'

# test = requests.get(f"{base_url}conversations.list", params={
#     'token': SLACK_API_KEY
# })
# channels = [x['id'] for x in test.json()['channels']]
# whitelisted_users = ['UMV2J37HD']

def delete_messages(channel_list, whitelisted_users):
    for channel in channel_list:
        try:
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
                    print(f"No username was found in message {message['ts']}")
        except KeyError:
            print(messages_history.content)

while True:
    conn = sqlite3.connect(DATABASE)
    conn.row_factory = sqlite3.Row
    cur = conn.cursor()
    cur.execute('''
                SELECT * FROM channels
                ''')
    all_data = cur.fetchall()
    conn.close()
    all_data_dict = []
    for row in all_data:
        channel = {
            'id': row['id'],
            'channel': row['channel'],
            'whitelist': row['whitelist'].split(',')
        }
        all_data_dict.append(channel)
    for row in all_data_dict:
        if row['channel'] and row['whitelist']:
            delete_messages([row['channel']], ",".join(row['whitelist']))
    time.sleep(5) 