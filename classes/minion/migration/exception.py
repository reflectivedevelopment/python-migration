

class minion_migration_exception(Exception):
    _migration = {}

    def __init__(self, message, migration, variables={}, code=0):
        self.value = message
        self._migration = migration
    def __str__(self):
        return repr(self.value)

    def get_migration(self):
        return self._migration
