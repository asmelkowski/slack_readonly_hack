import requests
import os
import time
from dotenv import load_dotenv

load_dotenv()
# Load API KEY stored in .env file (not ment for git tracking)
SLACK_API_KEY = os.getenv('SLACK_API_KEY')
base_url = 'https://slack.com/api/'

test = requests.get(f"{base_url}conversations.list", params={
    'token': SLACK_API_KEY
})
channels = [x['id'] for x in test.json()['channels']]
whitelisted_users = ['UMV2J37HD']

def delete_messages(channel_list, whitelisted_users):
    for channel in channels:
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

while True:
    delete_messages(['CMSN6JXL4'], whitelisted_users)
    time.sleep(5)