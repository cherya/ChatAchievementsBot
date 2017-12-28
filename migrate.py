from models.db import database
from models.models import *
from playhouse.migrate import *

from datetime import date

migrator = PostgresqlMigrator(database)

database.connect()

date_field = DateField(null=True)

migrate(
    migrator.add_column('statistic', 'date', date_field)
)

id_date = {
    '20170706': date(2017, 7, 6),
    '20170707': date(2017, 7, 7),
    '20170708': date(2017, 7, 8),
    '20170709': date(2017, 7, 9)
}

for key, val in id_date.items():
    stat = Statistic.get(Statistic.id == int(key))
    stat.date = val
    stat.save()
