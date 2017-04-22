from models import *
from db import database
from config import BaseConfig

from pprint import pprint
import telepot
import logging
import os
import time

dir_name = os.path.dirname(os.path.abspath(__file__))
logging.basicConfig(filename=dir_name+'/bot.log', level=logging.INFO, format='%(levelname)s:%(message)s')

cfg = BaseConfig.__dict__

if 'LISTEN_CHAT' in cfg:
    chats = [cfg['LISTEN_CHAT']]
    print(chats)
else:
    chats = []

bot = telepot.Bot(token=cfg['TOKEN'])
print(cfg['TOKEN'])


def run_bot_loop():
    print('Listening ...')
    bot.message_loop({
        'chat': handle_message,
        'edited_chat': handle_edit
    })


def handle_message(msg):
    print(msg)
    flavor = telepot.flavor(msg)
    content_type, chat_type, chat_id = telepot.glance(msg, flavor=flavor)
    if len(chats) == 0 or chat_id in chats:
        # just save every message
        database.connect()
        message = Messages.create(id=msg['message_id'], message=msg, chat_id=chat_id, content_type=content_type)
        message.save()
        database.close()
        pprint(msg)


# TODO: handle message edit
def handle_edit(msg):
    pass

