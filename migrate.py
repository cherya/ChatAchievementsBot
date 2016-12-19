from models.db import database
from models.models import *

database.connect()

achievement = Achievement.select().where((Achievement.name == 'Социоблядь'))

counters = UserAchievementCounters.select().where(UserAchievementCounters.achievement == achievement)

for counter in counters:
    if 'replied_to' in counter.counters:
        counter.value = 0
        counter.level = 0
        counter.counters['replied_to'] = []
        counter.save()

