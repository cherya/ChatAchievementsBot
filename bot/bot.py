from models.models import *
from models.db import database

import telepot
from pprint import pprint
import json

# for now let hardcode test chat and private
# TEST_CHAT_ID = -1001072621302

ADDMETO_CHAT_ID = -1001005702961

chats = [ADDMETO_CHAT_ID, 29462028]

config = json.load(open('config.json', encoding='utf-8'))

bot = telepot.Bot(token=config['token'])


def run_bot_loop():
    print('Listening ...')
    bot.message_loop({
        'chat': handle_message,
        'edited_chat': handle_edit
    })


def handle_message(msg):
    flavor = telepot.flavor(msg)
    content_type, chat_type, chat_id = telepot.glance(msg, flavor=flavor)
    if chat_id in chats:
        # just save every message
        database.connect()
        message = Messages.create(id=msg['message_id'], message=msg, chat_id=chat_id, content_type=content_type)
        message.save()
        database.close()
        pprint(msg)


def handle_edit(msg):
    pass


__all__ = ['run_bot_loop', 'bot', 'ADDMETO_CHAT_ID']
