from bot.tlgtm_bot import Bot
from models.models import *
from models.db import database
from bot.updater import update

import time
from pprint import pprint
import json

config = json.load(open('config.json', encoding='utf-8'))
LOG_CHAT_ID = '@addmetoachievements'
UPDATE_TIMEOUT = 1


class App:
    bot = None
    updater = None

    def __init__(self, bot):
        self.bot = bot(config['token'], self)

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
                text = '{0} achieved \'{1}\' LVL.{2}'.format(name, achievement['name'], achievement['level'])
                self.bot.send_message(LOG_CHAT_ID, text)


app = App(Bot)
# run message loop
app.run()

while True:
    # every UPDATE_TIMEOUT read new messages, count them, and delete
    update(app)
    time.sleep(UPDATE_TIMEOUT)
