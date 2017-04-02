import os
from slackclient import SlackClient
import security_keys


slack_client = SlackClient(security_keys.SLACK_BOT_TOKEN)

class Bot(object):


    @classmethod
    def start_server(cls):
        api_call = slack_client.api_call("users.list")
        if api_call.get('ok'):
            # retrieve all users so we can find our bot
            users = api_call.get('members')
            for user in users:
                if 'name' in user and user.get('name') == security_keys.BOT_NAME:
                    print("Bot ID for '" + user['name'] + "' is " + user.get('id'))
        else:
            print("could not find bot user with the name " + security_keys.BOT_NAME)
