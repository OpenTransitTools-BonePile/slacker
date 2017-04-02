from slackclient import SlackClient
import security_keys

from ott.utils import slack_utils


class Bot(object):
    """ a lot of code borrowed from fullstack article  
        @see https://www.fullstackpython.com/blog/build-first-slack-bot-python.html
    """
    def __init__(self):
        super(Bot, self).__init__()
        slack_client = SlackClient(security_keys.SLACK_BOT_TOKEN)
        bot_id = slack_utils.get_bot_id(slack_client, security_keys.BOT_NAME)
        if bot_id:
            slack_utils.connect_to_slack(slack_client, bot_id, self.slack_responder)

    def slack_responder(self, slack_client, command, channel):
        """ Receives commands directed at the bot and determines if they are valid commands. 
            If so, then acts on the commands. If not, returns back an "I don't know" message...
            
        """
        response = "What does '{}' mean?".format(command)
        if command.startswith('dd '):
            response = "Sure...write some more code then I can '{}'!".format(command)
        if "wing" in command or "zero" in command:
            response = "all your base are belong to us, so... {}".format(command)
        slack_client.api_call("chat.postMessage", channel=channel, text=response, as_user=True)

    @classmethod
    def start_server(cls):
        bot = Bot()
