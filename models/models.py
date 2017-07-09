from playhouse.postgres_ext import *
from .db import database
from datetime import datetime


class BaseModel(Model):
    class Meta:
        database = database


class User(BaseModel):
    id = CharField(primary_key=True)
    username = CharField(null=True)
    first_name = CharField(null=True)
    last_name = CharField(null=True)
    experience = IntegerField(default=0)

    def __str__(self):
        if not self.username is None:
            return self.username
        else:
            name = self.first_name
            if self.last_name is not None:
                name += ' ' + self.last_name
        return name


class Achievement(BaseModel):
    id = PrimaryKeyField()
    levels = ArrayField(null=True)
    name = CharField(default='achievement', unique=True)

    def __str__(self):
        return self.name


class UserAchievementCounters(BaseModel):
    user = ForeignKeyField(User)
    achievement = ForeignKeyField(Achievement)
    level = IntegerField(default=0)
    counters = JSONField(null=True)
    value = FloatField(default=0)
    date_achieved = DateTimeField(null=True)
    # chat_id = CharField()

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


class Messages(BaseModel):
    id = PrimaryKeyField()
    message = JSONField()
    date = DateTimeField(default=datetime.now)
    chat_id = CharField()
    content_type = CharField()


class Statistic(BaseModel):
    id = PrimaryKeyField()
    date = DateField(unique=True)
    messages = ArrayField(IntegerField, null=True)
    users = JSONField(default={})

database.connect()

database.create_tables(
    [User, Achievement, UserAchievementCounters, UserCounters, Messages, Statistic],
    safe=True
)

database.close()

__all__ = ['User', 'Achievement', 'UserAchievementCounters', 'UserCounters', 'Messages', 'Statistic']