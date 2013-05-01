from config import migration as migration_conf
from classes.minion.migration import base
from classes.minion.database import sqlalchemy
from classes.minion.migration import database

print migration_conf.conf()
migration = base.minion_migration_base({'group':'bla'})

print database.faux_instance('bla', migration_conf.conf())

print sqlalchemy.minion_database_sqlalchemy('bla', migration_conf.conf())

