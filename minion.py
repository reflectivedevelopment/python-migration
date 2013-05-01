from config import migration as migration_conf
#from classes.minion.migration import base
from classes.minion.database import mysql, base
from classes.minion.migration import database

object = mysql.minion_database_mysql('bla', migration_conf.conf()['connections']['default'])

for row in object.query(base.minion_database_base.SELECT, "select * from test"):
    print row

