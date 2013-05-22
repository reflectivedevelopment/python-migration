from config import migration as migration_conf
#from classes.minion.migration import base
from classes.minion.database import mysql, base
from classes.minion.migration import database

object = base.instance()

response =  object.query(base.minion_database_base.SELECT, "SELECT * FROM `test`")
for r in response:
    print r
#print object.query(base.minion_database_base.INSERT, "INSERT INTO `test` (i) VALUES (4)")

import classes.minion.migration.manager as manager

m = manager.minion_migration_manager(object)

m.run_migration();


