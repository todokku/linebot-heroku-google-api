from flask import Flask, request, abort

from linebot import (
    LineBotApi, WebhookHandler
)
from linebot.exceptions import (
    InvalidSignatureError
)
from linebot.models import *

app = Flask(__name__)

# Channel Access Token
line_bot_api = LineBotApi('absgdysguydgsuygduy')
# Channel Secret
handler = WebhookHandler('syudyiusyduiysd')


# Listen post request of /callback
@app.route("/callback", methods=['POST'])
def callback():
    # get X-Line-Signature header value
    signature = request.headers['X-Line-Signature']
    # get request body as text
    body = request.get_data(as_text=True)
    app.logger.info("Request body: " + body)
    # handle webhook body
    try:
        handler.handle(body, signature)
    except InvalidSignatureError:
        abort(400)
    return 'OK'



from pullFlybotCsv import pull_from_gsheet
def query_data_by_subselect(user_msg):
    ret_string = ''
    json_obj = {}
    json_obj = pull_from_gsheet()
    print("[DBG] user_msg" + user_msg)
    print("[DBG] json_obj")
    print(json_obj)

    for dicts in json_obj:
        if dicts['country'] == user_msg:
            ret_string = ret_string + str(dicts) + '\n'

    return ret_string
    
    
# message handler
@handler.add(MessageEvent, message=TextMessage)
def handle_message(event):
    user_msg = event.message.text

    if user_msg == 'h' or user_msg == 'H':
        send_msg = "MENU\n "
        message = TextSendMessage(text=send_msg)
        line_bot_api.reply_message(event.reply_token, message)

    elif user_msg == 'a':
        send_msg = "-- Country -- \n US \n UK \n NL\n "
        message = TextSendMessage(text=send_msg)
        line_bot_api.reply_message(event.reply_token, message)

#    else:
#        message = TextSendMessage(text=event.message.text)
#        line_bot_api.reply_message(event.reply_token, message)
    else:
        send_msg = query_data_by_subselect(user_msg)
        message = TextSendMessage(text=send_msg)
        line_bot_api.reply_message(event.reply_token, message)


import os
if __name__ == "__main__":
    port = int(os.environ.get('PORT', 5000))
    app.run(host='0.0.0.0', port=port)