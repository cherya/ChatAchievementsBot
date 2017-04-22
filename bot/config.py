import os


class BaseConfig(object):
    DEBUG = os.environ['DEBUG']
    DB_NAME = os.environ['DB_NAME']
    DB_USER = os.environ['DB_USER']
    DB_PASS = os.environ['DB_PASS']
    DB_PORT = os.environ['DB_PORT']
    DB_SERVICE = os.environ['DB_SERVICE']
    DATABASE_URI = 'postgresql://{0}:{1}@{2}:{3}/{4}'.format(
       DB_USER, DB_PASS, DB_SERVICE, DB_PORT, DB_NAME
    )
    TOKEN = os.environ['TOKEN']
    LOG_CHAT = os.environ['LOG_CHAT']
    LISTEN_CHAT = os.environ['LISTEN_CHAT']


# class BaseConfig(object):
#    DEBUG = True
#    DB_NAME = 'achievements'
#    DB_USER = ''
#    DB_PASS = ''
#    DB_PORT = '5432'
#    DB_SERVICE = 'postgres'
#    DATABASE_URI = 'postgresql://{0}:{1}@{2}:{3}/{4}'.format(
#       DB_USER, DB_PASS, DB_SERVICE, DB_PORT, DB_NAME
#    )
#    TOKEN = '265512459:AAF1L5Dx76PjwCP6Ei2HpSsOYBC07GpA2mA'
#    LOG_CHAT = '29462028'
#    LISTEN_CHAT = '29462028'