
from classes.minion.database.base import minion_database_base

# Creates a disposable instance of the faux connection

# param array Config for the underlying DB connection
# return minion_migration_database

def faux_instance(db_group, config):
    if config is None:
        if db_group is None:
            raise Exception("No database selected, and no default database exists!")

        raise Exception("No config specified, and no config exists!")

    return minion_migration_database('__minion_faux', config)

class minion_migration_database(minion_database_base):

    # The query stack used to store queries
    # var array

    _queries = []

    # Gets the stack of queries that have been executed

    def get_query_stack(self):
        return self._queries

    # Resets the query stack to an empty state and returns the queries

    # return ARray of SQL queries that would've been executed
    def reset_query_stack(self):
        queries = self._queries

        self._queries = []

        return queries

    # Appears to allow calling script to execute an SQL query, but merely log
    # it and returns NULL

    # return NULL
    def query(self, type, sql, as_object = False, params = None):
        self._queries.append(sql)

        return None
