from classes.minion.task.migrations.run import minion_task_migrations_run

task = minion_task_migrations_run()

task.execute(config={'group': 'test'})
