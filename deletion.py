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

def delete_messages(channel_list, whitelisted_users):
    print(f"Channel list: {channel_list}, whitelist: {whitelisted_users}")
    for channel in channel_list:
        try:
            messages_history = requests.get(f"{base_url}conversations.history", params={
                'token': SLACK_API_KEY,
                'channel': channel
            })
            for message in messages_history.json()['messages']:
                if message['user'] not in whitelisted_users:
                    delete_request = requests.post(f"{base_url}chat.delete", data={
                        'token': SLACK_API_KEY,
                        'channel': channel,
                        'ts': message['ts']
                    })
                    try:
                        thread_messages = requests.get(f"{base_url}channels.replies", params={
                            'token': SLACK_API_KEY,
                            'channel': channel,
                            'thread_ts': message['thread_ts']
                        }).json()
                        for reply in thread_messages['messages']:
                            if reply['user'] not in whitelisted_users:
                                requests.post(f"{base_url}chat.delete", data={
                                    'token': SLACK_API_KEY,
                                    'channel': channel,
                                    'ts': reply['ts']
                                })
                    except KeyError:
                        pass
                else:
                    try:
                        for reaction in message['reactions']:
                            for reaction_user in reaction['users']:
                                if reaction_user not in whitelisted_users:
                                    rmv_reaction = requests.get(f"{base_url}reactions.remove", params={
                                        'token': SLACK_API_KEY,
                                        'name': reaction['name'],
                                        'channel': channel,
                                        'timestamp': message['ts']
                                    })
                    except KeyError as e:
                        pass
                    # try:
                    #     reactions = requests.get(f"{base_url}reactions.get", params={
                    #         'token': SLACK_API_KEY,
                    #         'channel': channel,
                    #         'timestamp': message['ts']
                    #     })
                    #     print(reactions.content)
                    # except Exception as e:
                    #     print(e)
        except KeyError:
            return messages_history.content

<<<<<<< Updated upstream
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
=======
def run_all():
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
                'channels': row['channel'].split(','),
                'whitelist': row['whitelist'].split(',')
            }
            all_data_dict.append(channel)
        for row in all_data_dict:
            if row['channels'] and row['whitelist']:
                delete_messages(row['channels'], ",".join(row['whitelist']))
        time.sleep(5)
>>>>>>> Stashed changes


if __name__ == "__main__":
    delete_messages('CMFNQ0YR0', ['UMT3G1XN0'])