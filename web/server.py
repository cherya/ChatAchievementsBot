from flask import Flask
from flask import g
from flask import request
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


@app.before_request
def before_request():
    g.db = database
    g.db.connect()


@app.after_request
def after_request(response):
    g.db.close()
    return response


@app.route('/users/<user_id>/')
def user_detail(user_id, **kwargs):
    user = get_object_or_404(User, User.id == user_id)
    user_achievements = UserAchievementCounters.select().where(
        UserAchievementCounters.user == user,
        UserAchievementCounters.level > 0
    )
    counters = UserCounters.select().where(UserCounters.user == user)

    kwargs['user'] = user
    kwargs['counters'] = counters[0]
    kwargs['achievements_list'] = user_achievements
    return render_template('user_detail.html', **kwargs)


@app.route('/')
def homepage(**kwargs):
    counters = UserCounters.select()

    last_achievements = UserAchievementCounters.select().where(
        UserAchievementCounters.level > 0
    ).order_by(
        -UserAchievementCounters.date_achieved
    )[:20]

    total = {
        'user': 0,
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

    total['average_msg_length'] = round(total['average_msg_length'] / total['user'], 2)

    kwargs['total'] = total
    kwargs['counters_list'] = counters
    kwargs['achievements_list'] = last_achievements
    return render_template('homepage.html', **kwargs)
