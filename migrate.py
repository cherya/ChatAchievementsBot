from models.db import database
from models.models import *

database.connect()

achievement = Achievement.select().where((Achievement.name == 'Джугашвили') | (Achievement.name == 'Нигилист'))
UserAchievementCounters.delete().where(UserAchievementCounters.achievement << achievement).execute()


achievement = Achievement.get(Achievement.name == 'Микроблоггер')
counters = UserAchievementCounters.select().where(UserAchievementCounters.achievement == achievement,
                                                  UserAchievementCounters.level > 1)

for counter in counters:
    counter.level = 1
    counter.save()

database.close()
