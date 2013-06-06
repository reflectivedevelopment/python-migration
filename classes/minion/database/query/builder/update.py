from where import database_query_builder_where
from classes.minion.database.base import minion_database_base as database

#<?php defined('SYSPATH') OR die('No direct script access.');
#/**
# * Database query builder for UPDATE statements. See [Query Builder](/database/query/builder) for usage and examples.
# */
class database_query_builder_update(database_query_builder_where):

#	/**
#	 * Set the table for a update.
#	 *
#	 * @param   mixed  $table  table name or array($table, $alias) or object
#	 * @return  void
#	 */
    def __init__(self, table = None):
   #	// UPDATE ...
        self._table = None
    #
    #	// SET ...
        self._set = dict()
        if table:
#                       // Set the inital table name
            self._table = table

#               // Start the query with no SQL
        database_query_builder_where.__init__(self, database.UPDATE, '')
#
#	/**
#	 * Sets the table to update.
#	 *
#	 * @param   mixed  $table  table name or array($table, $alias) or object
#	 * @return  $this
#	 */
    def table(self, table):
        self._table = table

        return self

#	/**
#	 * Set the values to update with an associative array.
#	 *
#	 * @param   array   $pairs  associative (column => value) list
#	 * @return  $this
#	 */
    def set(self, pairs):
        for column in pairs:
            self._set[column] = pairs[column]

        return self

#	/**
#	 * Set the value of a single column.
#	 *
#	 * @param   mixed  $column  table name or array($table, $alias) or object
#	 * @param   mixed  $value   column value
#	 * @return  $this
#	 */
    def value(self, column, value):
       self._set[column] = value

       return self

#	/**
#	 * Compile the SQL query and return it.
#	 *
#	 * @param   object  $db  Database instance
#	 * @return  string
#	 */
    def compile(self, db):
#		// Start an update query
        query = 'UPDATE %s' % (db.quote_table(self._table))

#		// Add the columns to update
        query = '%s SET %s' % (query, self._compile_set(db, self._set))

        if len(self._where) > 0:
#			// Add selection conditions
            query = '%s WHERE %s' % (query, self._compile_conditions(db, self._where))

        if len(self._order_by) > 0:
            query = '%s %s' % (query, self._compile_order_by(db, self._order_by))

        if self._limit is not None:
            query = '%s LIMIT %s' % (query, self._limit)

        self._sql = query

        return database_query_builder_where.compile(self, db)

    def reset(self):
        self._table = None

        self._set = dict()
        self._where = []

        self._limit = None

        self._parameters = dict()

        self._sql = None

        return self
