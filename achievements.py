def reply_from(iid, msg):
    if 'reply_to_message' in msg:
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
    name = 'first message'

    def check(self, msg, content_type, global_counters, achievements_counters):
        print(global_counters['text'])
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
            if achievements_counters['reply_count'] > 1:
                return True


registered_achievements = [
    FirstMessage,
    StickerSpammer,
    SantaShpaker
]
