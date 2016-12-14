from models.db import database
from models.models import *

database.connect()

achievement = Achievement.select().where((Achievement.name == 'Социоблядь'))

counters = UserAchievementCounters.select().where(UserAchievementCounters.achievement == achievement)


for counter in counters:
    if 'replied_to' in counter.counters:
        if len(counter.counters['replied_to']) < 20:
            counter.level = 0
            counter.save()

