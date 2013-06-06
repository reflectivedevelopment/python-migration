from where import database_query_builder_where
from classes.minion.database.base import minion_database_base as database

#/**
# * Database query builder for DELETE statements. See [Query Builder](/database/query/builder) for usage and examples.
# *
# */
class database_query_builder_delete(database_query_builder_where):
#	/**
#	 * Set the table for a delete.
#	 *
#	 * @param   mixed  $table  table name or array($table, $alias) or object
#	 * @return  void
#	 */
    def __init__(self, table = None):
    #	// DELETE FROM ...
        self._table = None
        
        if table:
#			// Set the inital table name
            self._table = table

#		// Start the query with no SQL
        database_query_builder_where.__init__(self, database.DELETE, '')

#	/**
#	 * Sets the table to delete from.
#	 *
#	 * @param   mixed  $table  table name or array($table, $alias) or object
#	 * @return  $this
#	 */
    def table(self, table):
        self._table = table

        return self

#	/**
#	 * Compile the SQL query and return it.
#	 *
#	 * @param   object  $db  Database instance
#	 * @return  string
#	 */
    def compile(self, db):
#		// Start a deletion query
        query = 'DELETE FROM %s' % (db.quote_table(self._table))

        if len(self._where) > 0:
#			// Add deletion conditions
            query = '%s WHERE %s' % (query, self._compile_conditions(db, self._where)) 

        if len(self._order_by) > 0:
#			// Add sorting
            query = '%s %s' % (query, self._compile_order_by(db, self._order_by))

        if self._limit is not None:
            query = '%s LIMIT %s' % (query, self._limit)

        self._sql = query

        return database_query_builder_where.compile(self, db)

    def reset(self):
        self._table = None
        self._where = []

        self._parameters = dict()

        self._sql = None

        return self
