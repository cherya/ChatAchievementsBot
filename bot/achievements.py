import re

ADDMETO_CHANNEL = -1001005993407
TECHSPARKS_CHANNEL = -1001009962628
AN = 59645208

emoji_re = re.compile("["
        u"\U0001F600-\U0001F64F"
        u"\U0001F300-\U0001F5FF"
        u"\U0001F680-\U0001F6FF"
        u"\U0001F1E0-\U0001F1FF"
                           "]+", flags=re.UNICODE)

def get_msg_text(msg):
    text = ''
    if 'text' in msg:
        text = msg['text']
    if 'caption' in msg:
        text = msg['caption']
    return text

def re_from_str(str):
    str = re.escape(str)
    return re.compile(r'\b{0}\b'.format(str), re.IGNORECASE)

def reply_from(iid, msg):
    if is_reply(msg):
        return msg['reply_to_message']['from']['id'] == iid

def is_forward(msg):
    return 'forward_from' in msg or 'forward_from_chat' in msg

def msg_contains(msg, substr):
    if is_forward(msg):
        return False
    text = get_msg_text(msg)
    regexp = re_from_str(substr)
    contains = re.search(regexp, text)
    return True if contains is not None else False

def msg_contains_one_of(msg, substrs):
    text = get_msg_text(msg)
    for substr in substrs:
        now_contains = msg_contains(msg, substr)
        if now_contains:
            return True
    return False

def msg_equals(msg, str):
    text = get_msg_text(msg)
    regexp = re_from_str(str)
    return re.fullmatch(regexp, text)

def is_reply(msg):
    return 'reply_to_message' in msg

def is_self_reply(msg):
    if is_reply(msg):
        reply = msg['reply_to_message']
        return reply['from']['id'] == msg['from']['id']
    return False

def is_forward_from(msg, id):
    if 'forward_from_chat' in msg:
        return msg['forward_from_chat']['id'] == id
    if 'forward_from' in msg:
        return msg['forward_from']['id'] == id


class AchievementBase:
    name = None
    levels = []

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


class Flooder(AchievementBase):
    name = 'Флудер'
    levels = [100, 1000, 10000, 100000]

    def check(self, msg, content_type, counters, cur_level):
        return content_type == 'text'


class StickerSpammer(AchievementBase):
    name = 'Стикер-спаммер'
    levels = [10, 50, 200, 1000]

    def check(self, msg, content_type, counters, cur_level):
        return content_type == 'sticker'


class PontiusPilatus(AchievementBase):
    name = 'Понтий Пилат'
    levels = [10, 100, 1000, 5000]

    def check(self, msg, content_type, counters, cur_level):
        return reply_from(AN, msg)


class BackTo2007(AchievementBase):
    name = 'Назад в 2007'
    levels = [2, 10, 50, 200]

    def check(self, msg, content_type, counters, cur_level):
        if 'text' in msg:
            count = 0
            for emoji in emoji_re.finditer(msg['text']):
                s, e = emoji.span()
                count += e - s
            return count >= 5


class WhyDoYouAsk(AchievementBase):
    name = 'А ви таки зачем интересуетесь?'
    levels = [1, 10, 100, 500]

    def check(self, msg, content_type, counters, cur_level):
        count = 0
        if is_reply(msg) and content_type == 'text':
            reply = msg['reply_to_message']
            if not is_self_reply(msg) and 'text' in reply:
                _len = len(msg['text']) > 4 and len(reply['text']) > 4
                return reply['text'][-1] == '?' and msg['text'][-1] == '?' and _len


class Dzhugashvili(AchievementBase):
    name = 'Джугашвили'
    levels = [1, 5, 10, 50]

    def update(self, msg, content_type, achievements_counters):
        if achievements_counters is None:
            achievements_counters = {
                'links_in_row': 0
            }
        if content_type == 'text':
            links = re.findall('http[s]?://(?:[a-zA-Z]|[0-9]|[$-_@.&+]|[!*\(\),]|(?:%[0-9a-fA-F][0-9a-fA-F]))+',
                               msg['text'])

            if len(links) > 0:
                achievements_counters['links_in_row'] += 1
            else:
                achievements_counters['links_in_row'] = 0
        else:
            achievements_counters['links_in_row'] = 0

        return achievements_counters

    def check(self, msg, content_type, counters, cur_level):
        return counters['local']['links_in_row'] == 3


class KernelPanic(AchievementBase):
    name = 'Kernel Panic'
    levels = [1, 10, 100, 1000]

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
    levels = [1, 10, 100, 1000]

    def check(self, msg, content_type, counters, cur_level):
        if is_reply(msg):
            return msg['date'] - msg['reply_to_message']['date'] <= 5


class Ametist(AchievementBase):
    name = 'Я у мамы аметист'
    levels = [5, 20, 100, 1000]

    def check(self, msg, content_type, counters, cur_level):
        return msg_contains_one_of(msg, ['бог', 'бога', ' богу', 'богом'])

class PhotoReporter(AchievementBase):
    name = 'Фоторепортер'
    levels = [5, 50, 500, 2000]

    def check(self, msg, content_type, counters, cur_level):
        return content_type == 'photo'

class TNN(AchievementBase):
    name = 'Девственник'
    levels = [1, 5, 20, 100]

    def check(self, msg, content_type, counters, cur_level):
        return msg_contains_one_of(msg, ['тнн', 'тян не нужны'])

class Microblogger(AchievementBase):
    name = 'Микроблоггер'
    levels = [1, 5, 20, 100]

    def update(self, msg, content_type, achievements_counters):
        if achievements_counters is None:
            achievements_counters = {
                'messages_in_row': 1,
                'prev_msg_id': 0
            }

        msg_id = msg['message_id']

        if msg_id - 1 == achievements_counters['prev_msg_id']:
            achievements_counters['messages_in_row'] +=1
        else:
            achievements_counters['messages_in_row'] = 1

        achievements_counters['prev_msg_id'] = msg_id

        return achievements_counters

    def check(self, msg, content_type, counters, cur_level):
        return counters['local']['messages_in_row'] == 6


class Nigilist(AchievementBase):
    name = 'Нигилист'
    levels = [5, 20, 100, 1000]

    def check(self, msg, content_type, counters, cur_level):
        return msg_equals(msg, 'нет') or msg_equals(msg, 'no')

class Lolman(AchievementBase):
    name = 'Лiлка'
    levels = [2, 15, 50, 500]

    def check(self, msg, content_type, counters, cur_level):
        return msg_contains_one_of(msg, ['лол','охлол','lol','лал'])

class Zombie(AchievementBase):
    name = 'Зомби'
    levels = [1, 3, 10, 100]

    def check(self, msg, content_type, counters, cur_level):
        if is_reply(msg):
            return msg['date'] - msg['reply_to_message']['date'] >= 60*60*24  # more than 24 hours

class T800(AchievementBase):
    name = 'T800'
    levels = [1, 2, 5, 50]

    def check(self, msg, content_type, counters, cur_level):
        return is_forward_from(msg, ADDMETO_CHANNEL) or is_forward_from(msg, TECHSPARKS_CHANNEL)


class AddmetoReply(AchievementBase):
    name = 'Громозека'
    levels = [2, 15, 50]

    def check(self, msg, content_type, counters, cur_level):
        if is_reply(msg):
            chat_id = msg['reply_to_message']['chat']['id']
            return chat_id == ADDMETO_CHANNEL or chat_id == TECHSPARKS_CHANNEL


class PlusPlus(AchievementBase):
    name = 'Инкремент'
    levels = [3, 15, 50, 500]

    def check(self, msg, content_type, counters, cur_level):
        return msg_equals(msg, '+')


class BG(AchievementBase):
    name = 'Мама, я не могу больше пить'
    levels = [2, 10, 50, 200]

    def check(self, msg, content_type, counters, cur_level):
        return msg_contains(msg, 'б-г')


class SocialWhore(AchievementBase):
    name = 'Социоблядь'
    levels = [20, 50, 100, 300]

    def update(self, msg, content_type, achievements_counters):
        if achievements_counters is None:
            achievements_counters = {
                'replied_to': [],
                'new': False
            }

        if is_reply(msg) and not is_self_reply(msg):
            reply_id = msg['reply_to_message']['from']['id']
            achievements_counters['new'] = reply_id not in achievements_counters['replied_to']
            if achievements_counters['new']:
                achievements_counters['replied_to'].append(reply_id)
        else:
            achievements_counters['new'] = False
        return achievements_counters

    def check(self, msg, content_type, counters, cur_level):
        return counters['local']['new']


class Lisp(AchievementBase):
    name = '(list) ==>> NIL'
    levels = [2, 10, 50, 500]

    def check(self, msg, content_type, counters, cur_level):
        text = get_msg_text(msg)
        count = 0

        for c in text:
            if c == ')' or c == '(':
                count += 1
            else:
                return False
        return count >= 5

# никсельпиксель
class GoldenNicka(AchievementBase):
    name = 'Золотая Ника'
    levels = [3, 15, 50, 500]

    def check(self, msg, content_type, counters, cur_level):
        return msg_contains(msg, 'хуемразь')

# паста про суп 
class Dad(AchievementBase):
    name = 'Батя'
    levels = [30, 70, 150, 500]

    def check(self, msg, content_type, counters, cur_level):
        return msg_contains(msg, 'бля')

# упоротый папуг на арбузе 
class JesusHearMe(AchievementBase):
    name = 'Есус ты миня слышеш'
    levels = [5, 15, 70, 300]

    def check(self, msg, content_type, counters, cur_level):
        return msg_contains_one_of(msg, ['папуг', 'попугай'])

registered_achievements = [
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
    TNN,
    Microblogger,
    Nigilist,
    Lolman,
    Zombie,
    T800,
    BG,
    SocialWhore,
    Lisp,
    PlusPlus,
    AddmetoReply,
    GoldenNicka,
    Dad,
    JesusHearMe
]

__all__ = ['registered_achievements']
