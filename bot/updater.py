from db import database
from models import *
from achievements import registered_achievements
from bot import bot
from config import BaseConfig

from datetime import datetime

log_chat = None
cfg = BaseConfig.__dict__
if 'LOG_CHAT' in cfg:
    log_chat = cfg['LOG_CHAT']

achievement_instances = list(map((lambda achv: achv()), registered_achievements))


def update():
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
        if achieved:
            handle_achievements(user, achievements, msg)
    Messages.delete().where(Messages.id.in_(messages)).execute()
    database.close()


def user_from_msg(msg):
    user_id = msg['from']['id']
    user, created = User.get_or_create(id=user_id)

    user.username = msg['from']['username'] if 'username' in msg['from'] else None
    user.first_name = msg['from']['first_name'] if 'first_name' in msg['from'] else None
    user.last_name = msg['from']['last_name'] if 'last_name' in msg['from'] else None
    return user


# update global counters
def update_user_counters(msg, content_type):
    user = user_from_msg(msg)

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
        counters.average_msg_length = round(counters.sum_message_length / counters.messages, 2)
    elif content_type in counters.__dict__['_data']:
        counters.__dict__['_data'][content_type] += 1
    elif content_type == 'left_chat_member':
        counters.last_left_chat = msg['date']

    user.save()
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
        triggered = achievement.check(msg,
                                      content_type,
                                      {'global': global_counters, 'local': new_counters},
                                      achievements_counters.level)

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


def handle_achievements(user, achievements, msg):
    user = User.get(id=user)
    for achievement in achievements:
        name = user.first_name
        if user.username is not None:
            name = '@' + user.username
        text = '{0} получает \'{1}\' {2}го уровня за сообщение:'.format(name, achievement['name'], achievement['level'])
        if log_chat is not None:
            bot.sendMessage(log_chat, text)
            try:
               bot.forwardMessage(log_chat, msg['chat']['id'], msg['message_id'])
            except Exception as e:
               bot.sendMessage(log_chat, 'сообщение удалено')
            
        else:
            print(text)

__all__ = ['update']
