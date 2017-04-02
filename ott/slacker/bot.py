from slackclient import SlackClient
from textblob import TextBlob

from ott.utils import slack_utils
import security_keys

class Bot(object):
    def __init__(self):
        super(Bot, self).__init__()
        slack_client = SlackClient(security_keys.SLACK_BOT_TOKEN)
        bot_id = slack_utils.get_bot_id(slack_client, security_keys.BOT_NAME)
        if bot_id:
            slack_utils.connect_to_slack(slack_client, bot_id, self.slack_responder)


    def make_response(self, user_input):
        """ take raw text as input, process it with TextBlob, then formulate a proper response 
        :return: proper response to this input string
        """
        response = "What does '{}' mean?".format(user_input)
        text_blob = TextBlob(user_input)
        match, i = self.is_keyword(text_blob, 'geo')
        if match:
            response = "GeoCoding: '{}'!".format(self.strip(text_blob.words, s=i+1))
        else:
            from_match, i = self.is_keyword(text_blob, 'from', n=5)
            to_match, j = self.is_keyword(text_blob, 'to', s=i+1, n=10)
            if from_match and to_match:
                from_text = self.strip(text_blob.words, s=i+1, e=j-1)
                to_text = self.strip(text_blob.words, s=j+1)
                response = "TripPlanner F::{}, T::{}".format(from_text, to_text)
            else:
                match, i = self.is_keyword(text_blob, 'wing')
                if match:
                    r = self.strip(text_blob.words, s=i+1)
                    response = "all your base are belong to us, so... {}".format(r)
        return response

    def slack_responder(self, slack_client, command, channel):
        """ Receives commands directed at the bot and determines if they are valid commands. 
            If so, then acts on the commands. If not, returns back an "I don't know" message...
            
        """
        response = self.make_response(user_input=command)
        slack_client.api_call("chat.postMessage", channel=channel, text=response, as_user=True)

    @classmethod
    def start_server(cls):
        bot = Bot()
