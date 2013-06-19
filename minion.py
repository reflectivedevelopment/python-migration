from classes.minion.task.migrations.run import minion_task_migrations_run
from classes.minion.task.migrations.new import minion_task_migrations_new

task = minion_task_migrations_new()

task.execute(config={'group': 'dataminer/', 'description': 'test me now!'})

#task = minion_task_migrations_run()

#task.execute(config={'group': 'test'})
