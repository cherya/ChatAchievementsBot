from bot import Bot
from updater import Updater
from models import *
from pprint import pprint
import json

config = json.load(open('config.json', encoding='utf-8'))
LOG_CHAT_ID = '@addmetoachievements'


class App:
    bot = None
    updater = None

    def __init__(self, bot, updater):
        self.bot = bot(config['token'], self)
        self.updater = updater(self)

    def run(self):
        self.bot.run_forever()

    def handle_message(self, msg, content_type, chat_id):
        self.updater.message_update(msg, content_type, chat_id)
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

app = App(Bot, Updater)
app.run()
