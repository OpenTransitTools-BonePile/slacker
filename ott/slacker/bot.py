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

    @classmethod
    def is_keyword(cls, text_blob, keyword, n=1, s=0):
        """ see if keyword is in the first word (or first n words of the blob)
            :return both t/f for a match, and the index of the word where the match occurred
        """
        # import pdb; pdb.set_trace()
        match = False
        index = -1
        if text_blob:
            for i, word in enumerate(text_blob.words):
                if i < s:     # start the keyword search at index #i
                    continue
                if i >= n:    # don't evaluate more than n words deep
                    break
                suggestions = word.spellcheck()
                for suggestion in suggestions:
                    if suggestion[1] > 0.8:
                        if suggestion[0] == keyword.lower():
                            match = True
                            index = i
                            break
        return match, index

    def make_response(self, user_input):
        """ take raw text as input, process it with TextBlob, then formulate a proper response 
        :return: proper response to this input string
        """
        response = "What does '{}' mean?".format(user_input)
        text_blob = TextBlob(user_input)
        if self.is_keyword(text_blob, 'geo'):
            response = "GeoCoding: '{}'!".format(user_input)
        if self.is_keyword(text_blob, 'wing'):
            response = "all your base are belong to us, so... {}".format(user_input)
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
