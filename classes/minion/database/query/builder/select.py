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
        if len(columns) > 0:
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
        self._select = self._select + columns

        return self

#	/**
#	 * Choose the columns to select from, using an array.
#	 *
#	 * @param   array  $columns  list of column names or aliases
#	 * @return  $this
#	 */
    def select_array(self, columns):
        self._select = self._select + columns

        return self

#	/**
#	 * Choose the tables to select "FROM ..."
#	 *
#	 * @param   mixed  $table  table name or array($table, $alias) or object
#	 * @return  $this
#	 */
    def from_table(self, *tables):
        self._from = self._from + tables

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
#	public function group_by($columns)
#	{
#		$columns = func_get_args();
#
#		$this->_group_by = array_merge($this->_group_by, $columns);
#
#		return $this;
#	}
#
#	/**
#	 * Alias of and_having()
#	 *
#	 * @param   mixed   $column  column name or array($column, $alias) or object
#	 * @param   string  $op      logic operator
#	 * @param   mixed   $value   column value
#	 * @return  $this
#	 */
#	public function having($column, $op, $value = NULL)
#	{
#		return $this->and_having($column, $op, $value);
#	}
#
#	/**
#	 * Creates a new "AND HAVING" condition for the query.
#	 *
#	 * @param   mixed   $column  column name or array($column, $alias) or object
#	 * @param   string  $op      logic operator
#	 * @param   mixed   $value   column value
#	 * @return  $this
#	 */
#	public function and_having($column, $op, $value = NULL)
#	{
#		$this->_having[] = array('AND' => array($column, $op, $value));
#
#		return $this;
#	}
#
#	/**
#	 * Creates a new "OR HAVING" condition for the query.
#	 *
#	 * @param   mixed   $column  column name or array($column, $alias) or object
#	 * @param   string  $op      logic operator
#	 * @param   mixed   $value   column value
#	 * @return  $this
#	 */
#	public function or_having($column, $op, $value = NULL)
#	{
#		$this->_having[] = array('OR' => array($column, $op, $value));
#
#		return $this;
#	}
#
#	/**
#	 * Alias of and_having_open()
#	 *
#	 * @return  $this
#	 */
#	public function having_open()
#	{
#		return $this->and_having_open();
#	}
#
#	/**
#	 * Opens a new "AND HAVING (...)" grouping.
#	 *
#	 * @return  $this
#	 */
#	public function and_having_open()
#	{
#		$this->_having[] = array('AND' => '(');
#
#		return $this;
#	}
#
#	/**
#	 * Opens a new "OR HAVING (...)" grouping.
#	 *
#	 * @return  $this
#	 */
#	public function or_having_open()
#	{
#		$this->_having[] = array('OR' => '(');
#
#		return $this;
#	}
#
#	/**
#	 * Closes an open "AND HAVING (...)" grouping.
#	 *
#	 * @return  $this
#	 */
#	public function having_close()
#	{
#		return $this->and_having_close();
#	}
#
#	/**
#	 * Closes an open "AND HAVING (...)" grouping.
#	 *
#	 * @return  $this
#	 */
#	public function and_having_close()
#	{
#		$this->_having[] = array('AND' => ')');
#
#		return $this;
#	}
#
#	/**
#	 * Closes an open "OR HAVING (...)" grouping.
#	 *
#	 * @return  $this
#	 */
#	public function or_having_close()
#	{
#		$this->_having[] = array('OR' => ')');
#
#		return $this;
#	}
#
#	/**
#	 * Adds an other UNION clause.
#	 *
#	 * @param mixed $select  if string, it must be the name of a table. Else
#	 *  must be an instance of Database_Query_Builder_Select
#	 * @param boolean $all  decides if it's an UNION or UNION ALL clause
#	 * @return $this
#	 */
#	public function union($select, $all = TRUE)
#	{
#		if (is_string($select))
#		{
#			$select = DB::select()->from($select);
#		}
#		if ( ! $select instanceof Database_Query_Builder_Select)
#			throw new Kohana_Exception('first parameter must be a string or an instance of Database_Query_Builder_Select');
#		$this->_union []= array('select' => $select, 'all' => $all);
#		return $this;
#	}
#
#	/**
#	 * Start returning results after "OFFSET ..."
#	 *
#	 * @param   integer   $number  starting result number or NULL to reset
#	 * @return  $this
#	 */
#	public function offset($number)
#	{
#		$this->_offset = $number;
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
#	public function compile(Database $db)
#	{
#		// Callback to quote columns
#		$quote_column = array($db, 'quote_column');
#
#		// Callback to quote tables
#		$quote_table = array($db, 'quote_table');
#
#		// Start a selection query
#		$query = 'SELECT ';
#
#		if ($this->_distinct === TRUE)
#		{
#			// Select only unique results
#			$query .= 'DISTINCT ';
#		}
#
#		if (empty($this->_select))
#		{
#			// Select all columns
#			$query .= '*';
#		}
#		else
#		{
#			// Select all columns
#			$query .= implode(', ', array_unique(array_map($quote_column, $this->_select)));
#		}
#
#		if ( ! empty($this->_from))
#		{
#			// Set tables to select from
#			$query .= ' FROM '.implode(', ', array_unique(array_map($quote_table, $this->_from)));
#		}
#
#		if ( ! empty($this->_join))
#		{
#			// Add tables to join
#			$query .= ' '.$this->_compile_join($db, $this->_join);
#		}
#
#		if ( ! empty($this->_where))
#		{
#			// Add selection conditions
#			$query .= ' WHERE '.$this->_compile_conditions($db, $this->_where);
#		}
#
#		if ( ! empty($this->_group_by))
#		{
#			// Add grouping
#			$query .= ' '.$this->_compile_group_by($db, $this->_group_by);
#		}
#
#		if ( ! empty($this->_having))
#		{
#			// Add filtering conditions
#			$query .= ' HAVING '.$this->_compile_conditions($db, $this->_having);
#		}
#
#		if ( ! empty($this->_order_by))
#		{
#			// Add sorting
#			$query .= ' '.$this->_compile_order_by($db, $this->_order_by);
#		}
#
#		if ($this->_limit !== NULL)
#		{
#			// Add limiting
#			$query .= ' LIMIT '.$this->_limit;
#		}
#
#		if ($this->_offset !== NULL)
#		{
#			// Add offsets
#			$query .= ' OFFSET '.$this->_offset;
#		}
#
#		if ( ! empty($this->_union))
#		{
#			foreach ($this->_union as $u) {
#				$query .= ' UNION ';
#				if ($u['all'] === TRUE)
#				{
#					$query .= 'ALL ';
#				}
#				$query .= $u['select']->compile($db);
#			}
#		}
#
#		$this->_sql = $query;
#
#		return parent::compile($db);
#	}
#
#	public function reset()
#	{
#		$this->_select   =
#		$this->_from     =
#		$this->_join     =
#		$this->_where    =
#		$this->_group_by =
#		$this->_having   =
#		$this->_order_by =
#		$this->_union = array();
#
#		$this->_distinct = FALSE;
#
#		$this->_limit     =
#		$this->_offset    =
#		$this->_last_join = NULL;
#
#		$this->_parameters = array();
#
#		$this->_sql = NULL;
#
#		return $this;
#	}
#
#} // End Database_Query_Select
