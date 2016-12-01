from playhouse.postgres_ext import PostgresqlExtDatabase
import json

config = json.load(open('config.json', encoding='utf-8'))

DATABASE = config['database']
USER = config['user']
PASSWORD = config['password']

database = PostgresqlExtDatabase(DATABASE, user=USER, password=PASSWORD, host='localhost', register_hstore=False)
