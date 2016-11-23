from playhouse.postgres_ext import PostgresqlExtDatabase

DATABASE = 'achievements'
USER = ''
database = PostgresqlExtDatabase(DATABASE, user=USER, host='localhost', register_hstore=False)
