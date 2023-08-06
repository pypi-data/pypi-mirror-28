import os
import sys
import time
from slackclient import SlackClient
from slackbot_tipy.di import intent
from slackbot_tipy import bot_id

# constants
INIT_PROMPT = 'top'
try:
    AT_BOT = "@" + bot_id.get_id()
    CHANNEL = bot_id.get_group_id()
    print(CHANNEL)
except TypeError:
    pass

# instantiate client
slack_client = SlackClient(os.environ.get('SLACK_BOT_TOKEN'))

prompts = {}

def handle_command(command, channel):
    """
        Receives commands directed at the bot and determines if they
        are valid prompts. If so, then acts on the command/prompt. If not,
        returns back what it needs for clarification.
    """

    try:
        prompt_name = INIT_PROMPT if not prompts.get(channel) else prompts[channel]
        prompt_name, prompt, end_session = intent.decipher_intent(prompt_name,command)
        prompts[channel] = prompt_name if not end_session else INIT_PROMPT
        bot_response = prompt        

    except:
        exc_type, exc_obj, exc_tb = sys.exc_info()
        fname = os.path.split(exc_tb.tb_frame.f_code.co_filename)[1]
        bot_response = str(exc_type) + ', ' + str(exc_obj) + ', ' + fname + ', ' + str(exc_tb.tb_lineno)

    print("["+bot_response+"]")
    
    if len(bot_response) == 0:
        response = "Reset to top of tree."

    api_response = slack_client.api_call("chat.postMessage", channel=channel,
                                    text=bot_response, as_user=True)
    print(api_response)


def parse_slack_output(slack_rtm_output):
    """
        The Slack Real Time Messaging API is an events firehose.
        this parsing function returns None unless a message is
        directed at the Bot, based on its ID.
    """
    output_list = slack_rtm_output
    print(output_list)
    if output_list and len(output_list) > 0:
        for output in output_list:
            if output and 'text' in output and not 'bot_id' in output and output['channel'] == CHANNEL:
                # return text after the @ mention, whitespace removed
                return output['text'], output['channel']
    return None, None

if __name__ == "__main__":
    READ_WEBSOCKET_DELAY = 1 # 1 second delay between reading from firehose
    if slack_client.rtm_connect():
        print("StarterBot connected and running!")
        while True:
            command, channel = parse_slack_output(slack_client.rtm_read())
            print(command,channel)
            if command and channel:
                handle_command(command, channel)
                
            time.sleep(READ_WEBSOCKET_DELAY)
    else:
        print("Connection failed. Invalid Slack token or bot ID?")



