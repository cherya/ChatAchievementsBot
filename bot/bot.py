# -*- coding: utf-8 -*-
from models.models import *
from models.db import database
from config import config

from pprint import pprint
from datetime import datetime
import telepot
import logging
logging.basicConfig(filename='bot.log', level=logging.INFO, format='%(levelname)s:%(message)s')

# for now let hardcode test chat and private
# TEST_CHAT_ID = -1001072621302

ADDMETO_CHAT_ID = -1001005702961

chats = [ADDMETO_CHAT_ID, 29462028]

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
        username = msg['from']['username'] if 'username' in msg['from'] else msg['from']['id']

        logging.INFO('{0} [{1}] {2}: {3}'.format(datetime.fromtimestamp(msg['date']).strftime('%Y-%m-%d %H:%M:%S'),
                                                 username, content_type, msg[content_type]))

        pprint(msg)


def handle_edit(msg):
    pass


__all__ = ['run_bot_loop', 'bot', 'ADDMETO_CHAT_ID']
