import telepot

# for now let hardcode test chat and private
chats = [-1001072621302, 29462028]


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
