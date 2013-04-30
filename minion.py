from config import migration as migration_conf
from classes.minion.migration import base

print migration_conf.conf()
migration = base.minion_migration_base({'group':'bla'})
print migration.down(None)
