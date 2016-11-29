import re

emoji_re = re.compile("["
        u"\U0001F600-\U0001F64F"
        u"\U0001F300-\U0001F5FF"
        u"\U0001F680-\U0001F6FF"
        u"\U0001F1E0-\U0001F1FF"
                           "]+", flags=re.UNICODE)


def reply_from(iid, msg):
    if is_reply(msg):
        return msg['reply_to_message']['from']['id'] == iid


def msg_contains(msg, substr):
    contains = False
    text = ''
    if 'text' in msg:
        text = msg['text']
    if 'caption' in msg:
        text = msg['caption']

    text = text.upper()
    substr = substr.upper()
    
    contains = text.find(substr) > -1

    return contains

def is_reply(msg):
    return 'reply_to_message' in msg

def is_self_reply(msg):
    if is_reply(msg):
        reply = msg['reply_to_message']
        return reply['from']['id'] == msg['from']['id']
    return False


class AchievementBase:
    name = None
    levels = []

    def update(self, msg, content_type, achievements_counters):
        return achievements_counters

    # TODO: const
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

    def check(self, msg, content_type, counters, cur_level):
        return False

    def get_level(self, count):
        if count == 0:
            return 0

        if len(self.levels) > 0:
            for i in range(0, len(self.levels)):
                if count < self.levels[i]:
                    return i
            return i + 1
        else:
            return 0


class Welcome(AchievementBase):
    name = 'Добро пожаловать'
    levels = [1]

    def check(self, msg, content_type, counters, cur_level):
        return content_type == 'text'

class Flooder(AchievementBase):
    name = 'Флудер'
    levels = [100, 1000, 10000]

    def check(self, msg, content_type, counters, cur_level):
        return content_type == 'text'


class StickerSpammer(AchievementBase):
    name = 'Стикер-спаммер'
    levels = [10, 50, 200]

    def check(self, msg, content_type, counters, cur_level):
        return content_type == 'sticker'


class PontiusPilatus(AchievementBase):
    name = 'Понтий Пилат'
    levels = [10, 100, 1000]

    def check(self, msg, content_type, counters, cur_level):
        AN = 59645208
        return reply_from(AN, msg)


class BackTo2007(AchievementBase):
    name = 'Назад в 2007'
    levels = [2, 5, 10]

    def check(self, msg, content_type, counters, cur_level):
        if 'text' in msg:
            count = 0
            for emoji in emoji_re.finditer(msg['text']):
                s, e = emoji.span()
                count += e - s
            return count >= 5


class WhyDoYouAsk(AchievementBase):
    name = 'А ви таки зачем интересуетесь?'
    levels = [1, 10, 100]

    def check(self, msg, content_type, counters, cur_level):
        count = 0
        if is_reply(msg) and content_type == 'text':
            reply = msg['reply_to_message']
            if not is_self_reply(msg) and 'text' in reply:
                _len = len(msg['text']) > 4 and len(reply['text']) > 4
                return reply['text'][-1] == '?' and msg['text'][-1] == '?' and _len


class Dzhugashvili(AchievementBase):
    name = 'Джугашвили'
    levels = [1, 5, 10]

    def update(self, msg, content_type, achievements_counters):
        if achievements_counters is None:
            achievements_counters = {
                'links_in_row': 0
            }
        if content_type == 'text':
            links = re.findall('http[s]?://(?:[a-zA-Z]|[0-9]|[$-_@.&+]|[!*\(\),]|(?:%[0-9a-fA-F][0-9a-fA-F]))+',
                               msg['text'])
            entities_link = None
            if 'entities' in msg:
                for entitie in msg['entities']:
                    entities_link = entitie['type'] == 'text_link'

            if len(links) > 0 or entities_link is not None:
                achievements_counters['links_in_row'] += 1
            else:
                achievements_counters['links_in_row'] = 0
        else:
            achievements_counters['links_in_row'] = 0

        return achievements_counters

    def check(self, msg, content_type, counters, cur_level):
        return counters['local']['links_in_row'] >= 3


class KernelPanic(AchievementBase):
    name = 'Kernel Panic'
    levels = [5, 50, 500]

    def check(self, msg, content_type, counters, cur_level):
        text = ''
        count = 0
        if 'text' in msg:
            text = msg['text']
        if 'caption' in msg:
            text = msg['caption']

        for c in text:
            if c == 'A' or c == 'a' or c == 'А' or c == 'а':
                count += 1
            else:
                return False
        return count >= 5


class FastestHandInTheWest(AchievementBase):
    name = 'Быстрая рука'
    levels = [1, 10, 100]

    def check(self, msg, content_type, counters, cur_level):
        if is_reply(msg):
            return msg['date'] - msg['reply_to_message']['date'] <= 5


class Ametist(AchievementBase):
    name = 'Я у мамы аметист'
    levels = [5, 10, 100]

    def check(self, msg, content_type, counters, cur_level):
        return msg_contains(msg, ' бог')

class PhotoReporter(AchievementBase):
    name = 'Фоторепортер'
    levels = [5, 50, 500]

    def check(self, msg, content_type, counters, cur_level):
        return content_type == 'photo'

class TNN(AchievementBase):
    name = 'Девственник'
    levels = [1, 5, 20]

    def check(self, msg, content_type, counters, cur_level):
        return msg_contains(msg, ' тнн ') or msg_contains(msg, ' тян не нужны ')

registered_achievements = [
    Welcome,
    Flooder,
    StickerSpammer,
    PontiusPilatus,
    BackTo2007,
    WhyDoYouAsk,
    Dzhugashvili,
    KernelPanic,
    FastestHandInTheWest,
    Ametist,
    PhotoReporter,
    TNN
]

__all__ = ['registered_achievements']
