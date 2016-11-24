import re

emoji_re = re.compile("["
        u"\U0001F600-\U0001F64F"
        u"\U0001F300-\U0001F5FF"
        u"\U0001F680-\U0001F6FF"
        u"\U0001F1E0-\U0001F1FF"
                           "]+", flags=re.UNICODE)


def reply_from(iid, msg):
    if is_reply(msg):
        if msg['reply_to_message']['from']['id'] == iid:
            return True
    return False


def msg_contains(msg, substr):
    contains = False
    if 'text' in msg:
        contains = msg['text'].find(substr) > -1
    if 'caption' in msg:
        contains = msg['caption'].find(substr) > -1

    return contains

def is_reply(msg):
    if 'reply_to_message' in msg:
        return True
    return False

def is_self_reply(msg):
    if is_reply(msg):
        reply = msg['reply_to_message']
        if reply['from']['id'] == msg['from']['id']:
            return True
    return False

class AchievementBase:
    name = None

    def update(self, msg, content_type, achievements_counters):
        return achievements_counters

    # global_counters = {
    # 'forward_from_channel': int,
    # 'text': int,
    # 'game': int,
    # 'voice': int,
    # 'sticker': int,
    # 'document': int,
    # 'photo': int,
    # 'reply_to_message': int,
    # 'sum_message_length': int,
    # 'location': int,
    # 'messages': int,
    # 'video': int,
    # 'audio': int,
    # 'last_message_date': timestamp,
    # 'last_left_chat': timestamp,
    # 'forward': int,
    # 'average_msg_length': int
    # }
    # achievement_counters = any dict

    def check(self, msg, content_type, global_counters, achievements_counters):
        return False


class FirstMessage(AchievementBase):
    name = 'Добро пожаловать'

    def check(self, msg, content_type, global_counters, achievements_counters):
        if global_counters['text'] > 0:
            return True


class StickerSpammer(AchievementBase):
    name = 'sticker spammer'

    def check(self, msg, content_type, global_counters, achievements_counters):
        print(global_counters['sticker'])
        if global_counters['sticker'] >= 10:
            return True


class SantaShpaker(AchievementBase):
    name = 'Santa Shpaker'

    def update(self, msg, content_type, achievements_counters):
        # it's shpaker id
        if reply_from(9429534, msg):
            if achievements_counters is None:
                achievements_counters = {
                    'reply_count': 0
                }
            achievements_counters['reply_count'] += 1
        return achievements_counters

    def check(self, msg, content_type, global_counters, achievements_counters):
        if achievements_counters is not None:
            return achievements_counters['reply_count'] > 1


class BackTo2007(AchievementBase):
    name = 'Назад в 2007'

    def check(self, msg, content_type, global_counters, achievements_counters):
        if 'text' in msg:
            count = 0
            for emoji in emoji_re.finditer(msg['text']):
                s, e = emoji.span()
                count += e - s
            return count >= 5


class WhyDoYouAsk(AchievementBase):
    name = 'А ви таки зачем интересуетесь?'

    def update(self, msg, content_type, achievements_counters):
        count = 0
        if is_reply(msg) and content_type == 'text':
            reply = msg['reply_to_message']
            if not is_self_reply(msg) and 'text' in reply:
                if reply['text'][-1] == '?' and msg['text'][-1] == '?' and len(reply['text']) > 4 and len(msg['text']) > 4:
                    if achievements_counters is None:
                        achievements_counters = {
                            'questions_count': 0
                        }
                    achievements_counters['questions_count'] += 1
        return achievements_counters

    def check(self, msg, content_type, global_counters, achievements_counters):
        if achievements_counters is not None:
            return achievements_counters['questions_count'] > 5


registered_achievements = [
    FirstMessage,
    StickerSpammer,
    SantaShpaker,
    BackTo2007,
    WhyDoYouAsk
]

__all__ = ['registered_achievements']
