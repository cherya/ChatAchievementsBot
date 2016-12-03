from models.db import database
from playhouse.migrate import *

first_name_field = CharField(null=True, default=None)
last_name_field = CharField(null=True, default=None)

migrator = PostgresqlMigrator(database)

migrate(
    migrator.add_column('user', 'first_name', first_name_field),
    migrator.add_column('user', 'last_name', last_name_field)
)
