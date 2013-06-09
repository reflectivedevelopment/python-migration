from config import migration as migration_conf
#from classes.minion.migration import base
from classes.minion.database import mysql, base
from classes.minion.migration import database
from classes.minion.database import db

object = base.instance()

response =  object.query(base.minion_database_base.SELECT, "SELECT * FROM `test`")
for r in response:
    print r

print response.as_array()
print response.as_array('i')
print response.as_array('i','i')

print len(response)

print db.insert().table('test').columns('i').values(['1']).values(['2']).execute(object)
print db.select().from_table('test').where('i','=','1').execute(object).as_array()
print db.update().table('test').where('i','=','1').set({'i': '3'}).execute(object)
print db.delete().table('test').where('i','=','1').or_where('i','=','2').or_where('i','=','3').execute(object)
#print object.query(base.minion_database_base.INSERT, "INSERT INTO `test` (i) VALUES (5)")

import classes.minion.migration.manager as manager

#m = manager.minion_migration_manager(object)

#m.run_migration();

from classes.minion.task.migrations.run import minion_task_migrations_run

task = minion_task_migrations_run()

task.execute(config={'group': 'test'})
