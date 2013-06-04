from where import database_query_builder_where
from classes.minion.database.base import minion_database_base as database

#<?php defined('SYSPATH') OR die('No direct script access.');
#/**
# * Database query builder for SELECT statements. See [Query Builder](/database/query/builder) for usage and examples.
# */

class database_query_builder_select(database_query_builder_where):
    _select = []
    _distinct = False
    _from = []
    _join = []
    _group_by = []
    _having = []
    _offset = None
    _union = []
    _last_join = None

#	/**
#	 * Sets the initial columns to select from.
#	 *
#	 * @param   array  $columns  column list
#	 * @return  void
#	 */
    def __init__(self, columns = None):
        if columns is not None and len(columns) > 0:
            # Set the initial columns
            self._select = columns

        # Start the query with no actual SQL statement
        database_query_builder_where.__init__(self, database.SELECT, '')

#	/**
#	 * Enables or disables selecting only unique columns using "SELECT DISTINCT"
#	 *
#	 * @param   boolean  $value  enable or disable distinct columns
#	 * @return  $this
#	 */
    def distinct(self, value):
        self._distinct = bool(value)

        return self

#	/**
#	 * Choose the columns to select from.
#	 *
#	 * @param   mixed  $columns  column name or array($column, $alias) or object
#	 * @return  $this
#	 */
    def select(self, *columns):
        self._select = self._select + list(columns)

        return self

#	/**
#	 * Choose the columns to select from, using an array.
#	 *
#	 * @param   array  $columns  list of column names or aliases
#	 * @return  $this
#	 */
    def select_array(self, columns):
        self._select = self._select + list(columns)

        return self

#	/**
#	 * Choose the tables to select "FROM ..."
#	 *
#	 * @param   mixed  $table  table name or array($table, $alias) or object
#	 * @return  $this
#	 */
    def from_table(self, *tables):
        self._from = self._from + list(tables)

        return self

#	/**
#	 * Adds addition tables to "JOIN ...".
#	 *
#	 * @param   mixed   $table  column name or array($column, $alias) or object
#	 * @param   string  $type   join type (LEFT, RIGHT, INNER, etc)
#	 * @return  $this
#	 */
    def join(self, type=None):
        self._last_join = database_query_builder_join(table, type)
        self._join.append(self._last_join)

        return self

#	/**
#	 * Adds "ON ..." conditions for the last created JOIN statement.
#	 *
#	 * @param   mixed   $c1  column name or array($column, $alias) or object
#	 * @param   string  $op  logic operator
#	 * @param   mixed   $c2  column name or array($column, $alias) or object
#	 * @return  $this
#	 */
    def on(self, c1, op, c2):
        self._last_join_on(c1, op, c2)

        return self

#	/**
#	 * Adds "USING ..." conditions for the last created JOIN statement.
#	 *
#	 * @param   string  $columns  column name
#	 * @return  $this
#	 */
    def using(self, *columns):
        self._last_join.using(columns)

        return self

#	/**
#	 * Creates a "GROUP BY ..." filter.
#	 *
#	 * @param   mixed   $columns  column name or array($column, $alias) or object
#	 * @return  $this
#	 */
    def group_by(self, *columns):
        self._group_by = self._group_by + list(columns)

        return self

#	/**
#	 * Alias of and_having()
#	 *
#	 * @param   mixed   $column  column name or array($column, $alias) or object
#	 * @param   string  $op      logic operator
#	 * @param   mixed   $value   column value
#	 * @return  $this
#	 */
    def having(self, column, op, value = None):
        return self.and_having(column, op, value)

#	/**
#	 * Creates a new "AND HAVING" condition for the query.
#	 *
#	 * @param   mixed   $column  column name or array($column, $alias) or object
#	 * @param   string  $op      logic operator
#	 * @param   mixed   $value   column value
#	 * @return  $this
#	 */
    def and_having(self, columns, op, value = None):
        self._having.append({'AND': [column, op, value]})

        return self

#	/**
#	 * Creates a new "OR HAVING" condition for the query.
#	 *
#	 * @param   mixed   $column  column name or array($column, $alias) or object
#	 * @param   string  $op      logic operator
#	 * @param   mixed   $value   column value
#	 * @return  $this
#	 */
    def or_having(self, column, op, value = None):
        self._having.append({'OR': [column, op, value]})

        return self

#	/**
#	 * Alias of and_having_open()
#	 *
#	 * @return  $this
#	 */
    def having_open(self):
        return self.and_having_open()

#	/**
#	 * Opens a new "AND HAVING (...)" grouping.
#	 *
#	 * @return  $this
#	 */
    def and_having_open(self):
        self._having.append({'AND': '('})

        return self

#	/**
#	 * Opens a new "OR HAVING (...)" grouping.
#	 *
#	 * @return  $this
#	 */
    def or_having_open(self):
        self._having.append({'OR': '('})

        return self

#	/**
#	 * Closes an open "AND HAVING (...)" grouping.
#	 *
#	 * @return  $this
#	 */
    def having_close(self):
        return self.and_having_close()

#	/**
#	 * Closes an open "AND HAVING (...)" grouping.
#	 *
#	 * @return  $this
#	 */
    def and_having_close(self):
        self._having.append({'AND': ')'})

        return self
#
#	/**
#	 * Closes an open "OR HAVING (...)" grouping.
#	 *
#	 * @return  $this
#	 */
    def or_having_close(self):
        self._having.append({'OR': ')'})

        return self

#	/**
#	 * Adds an other UNION clause.
#	 *
#	 * @param mixed $select  if string, it must be the name of a table. Else
#	 *  must be an instance of Database_Query_Builder_Select
#	 * @param boolean $all  decides if it's an UNION or UNION ALL clause
#	 * @return $this
#	 */
#    def union(self, select, all=True):
#        if isinstance(select, str):
#            select = database.select().from_table(select)

# TODO
#		if ( ! $select instanceof Database_Query_Builder_Select)
#			throw new Kohana_Exception('first parameter must be a string or an instance of Database_Query_Builder_Select');
        self._union.append({'select': select, 'all': all})

        return self

#	/**
#	 * Start returning results after "OFFSET ..."
#	 *
#	 * @param   integer   $number  starting result number or NULL to reset
#	 * @return  $this
#	 */
    def offset(self, number):
       self._offset = number

       return self

#	/**
#	 * Compile the SQL query and return it.
#	 *
#	 * @param   object  $db  Database instance
#	 * @return  string
#	 */
    def compile(self, db):
#		// Callback to quote columns
#		$quote_column = array($db, 'quote_column');
#
#		// Callback to quote tables
#		$quote_table = array($db, 'quote_table');
#
#		// Start a selection query
        query = 'SELECT '

        if self._distinct:
#			// Select only unique results
            query = '%sDISTINCT ' % query

        if len(self._select) <= 0:
#			// Select all columns
            query = '%s*' % query
        else:
#			// Select all columns
            query = '%s%s' % (query, ', '.join( list( set ( [db.quote_column(x) for x in self._select] ) ) ) )

        if len(self._from) > 0:
            query = '%s FROM %s' % (query, ', '.join( list( set ( [db.quote_table(x) for x in self._from] ) ) ) )

        if len(self._join) > 0:
            query = '%s %s' % (query, self._compile_join(db, self._join))

        if len(self._where) > 0:
            query = '%s WHERE %s' % (query, self._compile_conditions(db, self._where))

        if len(self._group_by) > 0:
            query = '%s %s' % (query, self._compile_group_by(db, self._group_by))

        if len(self._having) > 0:
            query = '%s HAVING %s' % (query, self._compile_conditions(db, self._having))

        if len(self._order_by) > 0:
            query = '%s %s' % (query, self._compile_order_by(db, self._order_by))

        if self._limit is not None:
            query = '%s LIMIT %s' % (query, self._limit)

        if self._offset is not None:
            query = '%s OFFSET %s' % (query, self._offset)

        if len(self._union) > 0:
            for u in self._union:
                union_sql = ' UNION '
                if u['all']:
                    union_sql = '%s ALL ' % (union_sql)
                query = '%s %s %s' % (query, union_sql, u['select'].compile(db))

        self._sql = query

        return database_query_builder_where.compile(self, db)

    def reset(self):
        self._select = []
        self._distinct = False
        self._from = []
        self._join = []
        self._group_by = []
        self._having = []
        self._offset = None
        self._union = []
        self._last_join = None
        self._where = []
        self._order_by = []
        self._limit = None

        self._parameters = dict()

        self._sql = None

        return self
