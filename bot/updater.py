from models.db import database
from models.models import *
from .achievements import registered_achievements

from datetime import datetime

achievement_instances = list(map((lambda achv: achv()), registered_achievements))


def update(controller):
    database.connect()
    messages = Messages.select().order_by(Messages.date)
    # for every new message
    for message in messages:
        msg = message.message
        content_type = message.content_type
        chat_id = message.chat_id
        # update global counters
        counters = update_user_counters(msg, content_type)
        # check is any achievement triggered
        achieved, user, achievements = trigger_achievements(counters, msg, content_type, chat_id)
        controller.handle_achievement(achieved, user, achievements)
    Messages.delete().where(Messages.id.in_(messages)).execute()
    database.close()


# update global counters
def update_user_counters(msg, content_type):
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
    # chat is actually channel in telegram terms
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
        # get or create achievement model
        achievement_model, created = Achievement.get_or_create(name=achievement.name)
        achievement_model.levels = achievement.levels
        achievement_model.save()

        achievements_counters, created = UserAchievementCounters.get_or_create(user=user,
                                                                               achievement=achievement_model)

        # get updated achievement counters
        new_counters = achievement.update(msg, content_type, achievements_counters.counters)
        # check if achievement triggered
        triggered = achievement.check(msg, content_type, {'global': global_counters, 'local': new_counters}, )

        if triggered:
            achievements_counters.value += 1
            new_level = achievement.get_level(achievements_counters.value)
            if not new_level == achievements_counters.level:
                new_achievements.append({
                    'name': achievement.name,
                    'level': new_level
                })
                achieved = True
                achievements_counters.level = new_level
                achievements_counters.date_achieved = datetime.now()

        achievements_counters.counters = new_counters
        achievements_counters.save()

    return achieved, user, new_achievements


__all__ = ['update']
