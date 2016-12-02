from playhouse.postgres_ext import PostgresqlExtDatabase
from config import config

DATABASE = config['database']
USER = config['user']
PASSWORD = config['password']

database = PostgresqlExtDatabase(DATABASE, user=USER, password=PASSWORD, host='localhost', register_hstore=False)
