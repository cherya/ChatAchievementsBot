from flask import Flask
from flask import g
from flask import render_template
from flask import abort

from models.db import database
from models.models import *

app = Flask(__name__)
app.config.from_object(__name__)


def object_list(template_name, qr, var_name='object_list', **kwargs):
    kwargs[var_name] = qr
    return render_template(template_name, **kwargs)


def get_object_or_404(model, *expressions):
    try:
        return model.get(*expressions)
    except model.DoesNotExist:
        abort(404)


def get_totals_counters(counters):
    total = {
        'user': 0
    }
    for counter in counters:
        counter_dict = counter.__dict__['_data']
        for field in counter_dict:
            if not field == 'user':
                if field in total:
                    total[field] += counter_dict[field]
                else:
                    total[field] = counter_dict[field]
        total['user'] += 1
    total['average_msg_length'] = round(total['sum_message_length'] / total['messages'], 2)
    return total


def get_received_achievements():
    achievements = Achievement.select()
    received_achievements = []
    for achievement in achievements:
        times_received = UserAchievementCounters.select().where(
            UserAchievementCounters.level > 0,
            UserAchievementCounters.achievement == achievement
        ).count()
        if times_received > 0:
            received_achievements.append({
                'achievement': achievement,
                'times_received': times_received
            })
    received_achievements = sorted(received_achievements, key=lambda x: x['times_received'], reverse=True)
    return received_achievements


def get_top_users(amount):
    users = User.select()
    users_top = []
    for user in users:
        nmbr_achv = UserAchievementCounters.select().where(
            UserAchievementCounters.level > 0,
            UserAchievementCounters.user == user
        ).count()
        users_top.append({
            'user': user,
            'number_of_achievements': nmbr_achv
        })
    users_top = sorted(users_top, key=lambda x: x['number_of_achievements'], reverse=True)

    return users_top[:amount]


@app.before_request
def before_request():
    g.db = database
    g.db.connect()


@app.after_request
def after_request(response):
    g.db.close()
    return response


def get_achievement_progress(achievement):
    if len(achievement.achievement.levels) >= achievement.level:
        if achievement.level >= len(achievement.achievement.levels):
            return 1
        return round(achievement.value / achievement.achievement.levels[achievement.level], 2)


@app.route('/users/<user_id>/')
def user_detail(user_id):
    user = get_object_or_404(User, User.id == user_id)
    user_achievements = UserAchievementCounters.select().where(
        UserAchievementCounters.user == user,
        UserAchievementCounters.value > 0
    ).order_by(
        -UserAchievementCounters.level
    )
    counters = UserCounters.select().where(UserCounters.user == user)
    achievements = []
    for achievement in user_achievements:
        achievements.append({
            'level': achievement.level,
            'date_achieved': achievement.date_achieved,
            'achievement': achievement.achievement,
            'progress': get_achievement_progress(achievement)
        })

    context = {
        'user': user,
        'counters': counters[0],
        'achievements_list': achievements
    }
    return render_template('user_detail.html', **context)


@app.route('/achievements/<achievement_id>/')
def achievement_detail(achievement_id):
    achievement = get_object_or_404(Achievement, Achievement.id == achievement_id)
    users_received = UserAchievementCounters.select().where(
        UserAchievementCounters.level > 0,
        UserAchievementCounters.achievement == achievement_id
    ).order_by(
        -UserAchievementCounters.level
    )
    times_received = users_received.count()
    if times_received == 0:
        abort(404)

    context = {
        'counters': users_received,
        'achievement': achievement
    }
    return render_template('achievement_detail.html', **context)


@app.route('/')
def homepage():
    counters = UserCounters.select().order_by(
        -UserCounters.messages
    )

    last_achievements = UserAchievementCounters.select().where(
        UserAchievementCounters.level > 0
    ).order_by(
        -UserAchievementCounters.date_achieved
    )[:20]

    total = get_totals_counters(counters)
    received_achievements = get_received_achievements()
    top_users = get_top_users(15)

    context = {
        'total': total,
        'counters_list': counters,
        'achievements_list': last_achievements,
        'received_achievements': received_achievements,
        'achievements_count': Achievement.select().count(),
        'top_users': top_users
    }
    return render_template('homepage.html', **context)
