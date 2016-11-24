from bot import Bot
from db import database
from models import *
import time

import updater
from pprint import pprint
import json

config = json.load(open('config.json', encoding='utf-8'))
LOG_CHAT_ID = '@addmetoachievements'


class App:
    bot = None
    updater = None

    def __init__(self, bot):
        self.bot = bot(config['token'], self)

    def run(self):
        self.bot.run()

    def handle_message(self, msg, content_type, chat_id):
        database.connect()
        message = Messages.create(id=msg['message_id'], message=msg, chat_id=chat_id, content_type=content_type)
        message.save()
        database.close()
        pprint(msg)

    def handle_achievement(self, achieved, user, achievements):
        user = User.get(id=user)
        if achieved:
            for achievement in achievements:
                # username can be None T_T
                name = user.id
                if user.username is not None:
                    name = '@' + user.username
                text = '{0} achieved \'{1}\''.format(name, achievement.name)
                self.bot.send_message(LOG_CHAT_ID, text)


app = App(Bot)
app.run()

while True:
    print('updating...')
    updater.update(app)
    time.sleep(60)
