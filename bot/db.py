from config import BaseConfig

from playhouse.db_url import connect

conf = BaseConfig.__dict__
DATABASE = conf['DB_NAME']
USER = conf['DB_USER']
PASSWORD = conf['DB_PASS']
DATABASE_URI = conf['DATABASE_URI']

database = connect(DATABASE_URI)

# from playhouse.postgres_ext import PostgresqlExtDatabase

# DATABASE = conf['DB_NAME']
# USER = conf['DB_USER']
# PASSWORD = conf['DB_PASS']

# database = PostgresqlExtDatabase(DATABASE, user=USER, password=PASSWORD, host='localhost', register_hstore=False)