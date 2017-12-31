from models.models import *
from models.db import database
from config import config
import pprint
import telepot
import logging
import os

dir_name = os.path.dirname(os.path.abspath(__file__))
logging.basicConfig(filename=dir_name+'/bot.log', level=logging.INFO, format='%(levelname)s:%(message)s')

if 'listen_chats' in config:
    chats = config['listen_chats']
else:
    chats = []

bot = telepot.Bot(token=config['token'])


class PrettyPrinter(pprint.PrettyPrinter):
    def format(self, object, context, maxlevels, level):
        if isinstance(object, str):
            return (object.encode('utf8').decode(), True, False)
        return pprint.PrettyPrinter.format(self, object, context, maxlevels, level)

printer = PrettyPrinter()

def run_bot_loop():
    print('Listening ...')
    bot.message_loop({
        'chat': handle_message,
        'edited_chat': handle_edit
    })


def handle_message(msg):
    flavor = telepot.flavor(msg)
    content_type, chat_type, chat_id = telepot.glance(msg, flavor=flavor)
    if len(chats) == 0 or chat_id in chats:
        # just save every message
        database.connect()
        message = Messages.create(id=msg['message_id'], message=msg, chat_id=chat_id, content_type=content_type)
        message.save()
        database.close()
        printer.pprint(msg)


# TODO: handle message edit
def handle_edit(msg):
    pass


__all__ = ['run_bot_loop', 'bot']
