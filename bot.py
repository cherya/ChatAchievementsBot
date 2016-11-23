import asyncio
import telepot
import telepot
import telepot.namedtuple as nt


chats = [-162586002]


class Bot:
    def __init__(self, token, controller):
        self.bot = telepot.Bot(token)
        self.controller = controller

    def run_forever(self):
        print('Listening ...')
        self.bot.message_loop({
            'chat': self.handle_message
        }, run_forever=True)

    def handle_message(self, msg):
        flavor = telepot.flavor(msg)
        content_type, chat_type, chat_id = telepot.glance(msg, flavor=flavor)

        if self.controller is not None and chat_id in chats:
            self.controller.handle_message(msg, content_type, chat_id)

    def send_message(self, chat_id, msg):
        self.bot.sendMessage(chat_id, msg)

