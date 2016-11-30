from models.models import *
from models.db import database
from .updater import update

import telepot
import time
from pprint import pprint

LOG_CHAT_ID = '@addmetoachievements'
UPDATE_TIMEOUT = 30


# for now let hardcode test chat and private
# TEST_CHAT_ID = -1001072621302

ADDMETO_CHAT_ID = -1001005702961

chats = [ADDMETO_CHAT_ID, 29462028]


class Bot:
    def __init__(self, token, controller):
        self.bot = telepot.Bot(token)
        self.controller = controller

    def run(self):
        print('Listening ...')
        self.bot.message_loop({
            'chat': self.handle_message,
            'edited_chat': self.handle_edit
        })

    def handle_message(self, msg):
        flavor = telepot.flavor(msg)
        content_type, chat_type, chat_id = telepot.glance(msg, flavor=flavor)

        if self.controller is not None and chat_id in chats:
            self.controller.handle_message(msg, content_type, chat_id)

    def handle_edit(self):
        pass

    def send_message(self, chat_id, msg):
        self.bot.sendMessage(chat_id, msg)


class App:
    bot = None
    updater = None

    def __init__(self, token):
        self.bot = Bot(token, self)

    def run(self):
        self.bot.run()

    @staticmethod
    def handle_message(msg, content_type, chat_id):
        # just save every message
        database.connect()
        message = Messages.create(id=msg['message_id'], message=msg, chat_id=chat_id, content_type=content_type)
        message.save()
        database.close()
        pprint(msg)

    def handle_achievement(self, achieved, user, achievements):
        user = User.get(id=user)
        if achieved:
            for achievement in achievements:
                # TODO: username can be None T_T
                name = user.id
                if user.username is not None:
                    name = '@' + user.username
                text = '{0} получил \'{1}\' {2}го уровня'.format(name, achievement['name'], achievement['level'])
                self.bot.send_message(LOG_CHAT_ID, text)


def run_bot(token):
    app = App(token)
    # run message loop
    app.run()

    while True:
        # every UPDATE_TIMEOUT read new messages, count them, and delete
        update(app)
        time.sleep(UPDATE_TIMEOUT)
