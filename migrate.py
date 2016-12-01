from models.db import database
from models.models import *

database.connect()
achievement = Achievement.get(Achievement.name == 'Добро пожаловать')
UserAchievementCounters.delete().where(UserAchievementCounters.achievement == achievement).execute()
database.close()
