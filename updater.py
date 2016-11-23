from models import *
from achievements import registered_achievements
from db import database


achievement_instances = list(map((lambda achv: achv()), registered_achievements))


class Updater:
    controller = None

    def __init__(self, controller):
        self.controller = controller

    def message_update(self, msg, content_type, chat_id):
        database.connect()
        counters = get_user_counters(msg, content_type)
        achieved, user, achievements = trigger_achievements(counters, msg, content_type, chat_id)
        self.controller.handle_achievement(achieved, user, achievements)
        database.close()


def get_user_counters(msg, content_type):
    usr_id = msg['from']['id']
    username = None
    if 'username' in msg['from']:
        username = msg['from']['username']
    user, created = User.get_or_create(id=usr_id, username=username)
    counters, created = UserCounters.get_or_create(user=user)

    counters.__dict__['_data']['messages'] += 1
    counters.last_message_date = msg['date']

    if 'reply_to_message' in msg:
        counters.reply_to_message += 1
    # chat is actually group in telegram terms
    if 'forward_from_chat' in msg:
        counters.forward_from_channel += 1

    if content_type == 'text':
        counters.text += 1
        text = msg['text']
        counters.sum_message_length += len(text)
        counters.average_msg_length = counters.sum_message_length / counters.messages
    elif content_type in counters.__dict__['_data']:
        counters.__dict__['_data'][content_type] += 1
    elif content_type == 'left_chat_member':
        counters.last_left_chat = msg['date']

    counters.save()
    return counters.__dict__['_data']


def trigger_achievements(global_counters, msg, content_type, chat_id):
    achieved = False
    new_achievements = []
    user = global_counters['user']

    # for each achievement class create instance, update and check it
    for achievement in achievement_instances:
        achievement_model, created = Achievement.get_or_create(name=achievement.name)
        achievements_counters = None

        # check if user already get this achievement
        try:
            achievements_counters = UserAchievementCounters.get(user=user, achievement=achievement_model)
            already_achieved = achievements_counters.achieved
        except DoesNotExist:
            already_achieved = False

        if not already_achieved:
            if achievements_counters is None:
                achievements_counters, created = UserAchievementCounters.get_or_create(user=user,
                                                                                       achievement=achievement_model,
                                                                                       chat_id=chat_id)

            new_counters = achievement.get_updates(msg, achievements_counters.counters)

            if achievement.check(msg, content_type, global_counters, new_counters):
                achieved = True
                achievements_counters.achieved = True
                new_achievements.append(achievement)

            achievements_counters.counters = new_counters
            achievements_counters.save()

    return achieved, user, new_achievements
