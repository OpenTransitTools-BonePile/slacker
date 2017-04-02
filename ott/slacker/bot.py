import os
import time
from slackclient import SlackClient
import security_keys


slack_client = SlackClient(security_keys.SLACK_BOT_TOKEN)

EXAMPLE_COMMAND = "do"


class Bot(object):
    """ a lot of code borrowed from fullstack article  
        @see https://www.fullstackpython.com/blog/build-first-slack-bot-python.html
    """
    def __init__(self):
        super(Bot, self).__init__()
        bot_id = self.get_bot_id()
        if bot_id:
            at_bot = "<@{}>".format(bot_id)
            self.connect_to_slack(at_bot)

    @classmethod
    def get_bot_id(cls):
        bot_id = None
        api_call = slack_client.api_call("users.list")
        if api_call.get('ok'):
            # retrieve all users so we can find our bot
            users = api_call.get('members')
            for user in users:
                if 'name' in user and user.get('name') == security_keys.BOT_NAME:
                    print("Bot ID for '" + user['name'] + "' is " + user.get('id'))
                    bot_id = user.get('id')
                    break
        else:
            print("could not find bot user with the name " + security_keys.BOT_NAME)
        return bot_id

    @classmethod
    def handle_command(cls, command, channel):
        """
            Receives commands directed at the bot and determines if they
            are valid commands. If so, then acts on the commands. If not,
            returns back what it needs for clarification.
        """
        response = "Not sure what '{}' means...".format(command, EXAMPLE_COMMAND)
        if command.startswith(EXAMPLE_COMMAND):
            response = "Sure...write some more code then I can then '{}'!".format(command)
        slack_client.api_call("chat.postMessage", channel=channel, text=response, as_user=True)

    @classmethod
    def parse_slack_output(cls, slack_rtm_output, at_bot):
        """
            The Slack Real Time Messaging API is an events firehose.
            this parsing function returns None unless a message is
            directed at the Bot, based on its ID.
        """
        output_list = slack_rtm_output
        if output_list and len(output_list) > 0:
            for output in output_list:
                if output and 'text' in output and at_bot in output['text']:
                    # return text after the @ mention, whitespace removed
                    return output['text'].split(at_bot)[1].strip().lower(), output['channel']
        return None, None

    @classmethod
    def connect_to_slack(cls, at_bot):
        READ_WEBSOCKET_DELAY = 1  # 1 second delay between reading from firehose
        if slack_client.rtm_connect():
            print("StarterBot connected and running!")
            while True:
                command, channel = cls.parse_slack_output(slack_client.rtm_read(), at_bot)
                if command and channel:
                    cls.handle_command(command, channel)
                time.sleep(READ_WEBSOCKET_DELAY)
        else:
            print("Connection failed. Invalid Slack token or bot ID?")



    @classmethod
    def start_server(cls):
        bot = Bot()
