from where import database_query_builder_where
from classes.minion.database.base import minion_database_base as database

#<?php defined('SYSPATH') OR die('No direct script access.');
#/**
# * Database query builder for INSERT statements. See [Query Builder](/database/query/builder) for usage and examples.
# */
class database_query_builder_insert(database_query_builder_where):

#	/**
#	 * Set the table and columns for an insert.
#	 *
#	 * @param   mixed  $table    table name or array($table, $alias) or object
#	 * @param   array  $columns  column names
#	 * @return  void
#	 */
    def __init__(self, table=None, columns=None):
    #	// INSERT INTO ...
        self._table = None

    #	// (...)
        self._columns = []
    #
    #	// VALUES (...)
        self._values = []

        if table:
#			// Set the inital table name
            self._table = table

        if columns:
#			// Set the column names
            self._columns = columns

#		// Start the query with no SQL
        database_query_builder_where.__init__(self, database.INSERT, '')

#	/**
#	 * Sets the table to insert into.
#	 *
#	 * @param   mixed  $table  table name or array($table, $alias) or object
#	 * @return  $this
#	 */
    def table(self, table):
        self._table = table

        return self

#	/**
#	 * Set the columns that will be inserted.
#	 *
#	 * @param   array  $columns  column names
#	 * @return  $this
#	 */
    def columns(self, columns):
        self._columns = columns

        return self

#	/**
#	 * Adds or overwrites values. Multiple value sets can be added.
#	 *
#	 * @param   array   $values  values list
#	 * @param   ...
#	 * @return  $this
#	 */
    def values(self, values):
        if not isinstance(self._values, (tuple, list)):
            raise Exeception('INSERT INTO ... SELECT statements cannot be combined with INSERT INTO ... VALUES')

#		// Get all of the passed values
        values = [list(values)]

        self._values = self._values + values

        return self

#	/**
#	 * Use a sub-query to for the inserted values.
#	 *
#	 * @param   object  $query  Database_Query of SELECT type
#	 * @return  $this
#	 */
#	public function select(Database_Query $query)
#	{
#		if ($query->type() !== Database::SELECT)
#		{
#			throw new Kohana_Exception('Only SELECT queries can be combined with INSERT queries');
#		}
#
#		$this->_values = $query;
#
#		return $this;
#	}
#
#	/**
#	 * Compile the SQL query and return it.
#	 *
#	 * @param   object  $db  Database instance
#	 * @return  string
#	 */
    def compile(self, db):
#		// Start an insertion query
        query = 'INSERT INTO %s' % (db.quote_table(self._table))

#		// Add the column names
        query = '%s (%s) ' % (query, ', '.join([db.quote_column(c) for c in self._columns]))

        if isinstance(self._values, (list, tuple)):
#			// Callback for quoting values
#			$quote = array($db, 'quote');
#
            groups = []

            for group in self._values:
                offset = 0
                for value in group:
                    if isinstance(value, str) and not self._parameters.has_key(value):
#						// Quote the value, it is not a parameter
                        group[offset] = db.quote(value)
#
                    offset += 1
                groups.append('(%s)' % (', '.join(group)))

#			// Add the values
            query = '%s VALUES %s' % (query, ', '.join(groups))
        else:
#			// Add the sub-query
            query = '%s %s' % (query, str( self._values))

        self._sql = query

        return database_query_builder_where.compile(self, db)

    def reset(self):
       self._table = None

       self._columns = []
       self._values = []

       self._parameters = dict()

       self._sql = None

       return self
