

class AchievementBase:
    name = None

    def get_updates(self, msg, achievements_counters):
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
    # 'average_msg_length': timestamp
    # }
    # achievement_counters = any dict

    def check(self, msg, content_type, global_counters, achievements_counters):
        return False


class FirstMessage(AchievementBase):
    name = 'first message'

    def check(self, msg, content_type, global_counters, achievements_counters):
        if not global_counters['text'] > 0:
            return True


class StickerSpammer(AchievementBase):
    name = 'sticker spammer'

    def check(self, msg, content_type, global_counters, achievements_counters):
        if global_counters['sticker'] >= 10:
            return True


registered_achievements = [FirstMessage, StickerSpammer]
