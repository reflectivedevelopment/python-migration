from config import migration

#
# The base migration class, must be extended by all migration files
#
# Each migration file must implement an up() and a down() which are used to
# apply / remove this migration from the schema repspectively
#

# Abstract Class
class minion_migration_base():

    # array of information about this migration
    _info = dict()

    # construct the migration

    # param array Information about this migration
    def __init__(self, info):
        self._info = info

    # get the name of the database connection group this migration should be run against

    # return string
    def get_database_connection(self):
        config = migration.conf()
        group = self._info['group']

        if config.has_key(group):
            return config[group]

        raise Exception("No database was selected, and no defaults exist!")

    # Runs an SQL queries necessary to bring the database up a migration version

    # param db The database connectino to perform actions on 
    def up(self, db):
        raise NotImplementedError("Abstract")

    def down(self, db):
        raise NotImplementedError("Abstract")
