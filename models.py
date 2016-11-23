from playhouse.postgres_ext import *
from db import database


class BaseModel(Model):
    class Meta:
        database = database


class User(BaseModel):
    id = CharField(primary_key=True)
    username = CharField(null=True)
    experience = IntegerField(default=0)


class Achievement(BaseModel):
    id = PrimaryKeyField()
    name = CharField(default='achievement', unique=True)


class UserAchievementCounters(BaseModel):
    user = ForeignKeyField(User)
    achievement = ForeignKeyField(Achievement)
    counters = JSONField(null=True)
    achieved = BooleanField(default=False)
    chat_id = CharField()

    class Meta:
        primary_key = CompositeKey('user', 'achievement')


class UserCounters(BaseModel):
    user = ForeignKeyField(User)
    last_message_date = IntegerField(default=0)
    messages = IntegerField(default=0)
    text = IntegerField(default=0)
    forward = IntegerField(default=0)
    forward_from_channel = IntegerField(default=0)
    reply_to_message = IntegerField(default=0)
    audio = IntegerField(default=0)
    document = IntegerField(default=0)
    game = IntegerField(default=0)
    photo = IntegerField(default=0)
    sticker = IntegerField(default=0)
    video = IntegerField(default=0)
    voice = IntegerField(default=0)
    location = IntegerField(default=0)
    sum_message_length = BigIntegerField(default=0)
    average_msg_length = FloatField(default=0)
    last_left_chat = IntegerField(default=0)
    # last_enter_chat = IntegerField(default=0)


database.connect()
database.create_tables([User, Achievement, UserAchievementCounters, UserCounters], safe=True)
database.close()
