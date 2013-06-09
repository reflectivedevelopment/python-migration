
import re

# Get a singleton Database instance. If configruation is not specified,
# it will be loaded from the database configuration file using the same
# group as the name.

# param string name instance name
# param array config configuration parameters
# return Database
def instance(name = None, config = None):
    if name is None:
        name = minion_database_base.default

    if not minion_database_base.instances.has_key(name):
        if config is None:
            import config.migration as default_conf
            config = default_conf.conf()['connections'][name]
        if not config.has_key('type'):
            raise Exception("Database type not defined in configuration")

        # Create database connection instance
        try:
            db_module = __import__( 'classes.minion.database.%s' % config['type'], fromlist=['classes.minion.database.%s' % config['type']])
        except:
            raise Exception("Unable to load database type.")
        return db_module.instance(name=name, config=config);
    return minion_database_base.instances[name]

# Database connection wraper/helper.

# This class provides connection instance management via Database Drivers, as
# well as quoting, escaping and other related functions.

class minion_database_base():
    # Query types
    SELECT = 1
    INSERT = 2
    UPDATE = 3
    DELETE = 4

    # default instance name
    default = 'default'

    # database instances
    instances = dict()

    # @var  string  the last query executed
    last_query = None

    # Character that is used to quote identifiers
    _identifier = '"'

    # Instance name
    _instance = None

    # Raw server connection
    _connection = None

    # Configuration
    _config = None

    # TODO verify that these names are what we actually want to use
    def __init__(self, name, config):
        # set the instance name
        self._instance = name

        # store the config locally
        self._config = config

        if not self._config.has_key('table_prefix'):
            self._config['table_prefix'] = ''

        minion_database_base.instances[name] = self

    def __del__(self):
        self.disconnect()

    def connect(self):
        raise NotImplementedError("Abstract")

    def disconnect(self):
        del minion_database_base.instances[self._instance]

        return True

    # Set the connectino character set. This is called automatically by database connect
    def set_charset(self, charset):
        raise NotImplementedError("Abstract")
        
    #/*
    # * Perform an SQL query of the given type.
    # *
    # *     // Make a SELECT query and use objects for results
    # *     $db->query(Database::SELECT, 'SELECT * FROM groups', TRUE);
    # *
    # *     // Make a SELECT query and use "Model_User" for the results
    # *     $db->query(Database::SELECT, 'SELECT * FROM users LIMIT 1', 'Model_User');
    # *
    # * @param   integer  $type       Database::SELECT, Database::INSERT, etc
    # * @param   string   $sql        SQL query
    # * @param   mixed    $as_object  result object class string, TRUE for stdClass, FALSE for assoc array
    # * @param   array    $params     object construct parameters for result class
    # * @return  object   Database_Result for SELECT queries
    # * @return  array    list (insert id, row count) for INSERT queries
    # * @return  integer  number of affected rows for all other queries
    # */
    def query(self, type, sql, as_object=False, params=None):
        raise NotImplementedError("Abstract")

    #/**
    # * Start a SQL transaction
    # *
    # *     // Start the transactions
    # *     $db->begin();
    # *
    # *     try {
    # *          DB::insert('users')->values($user1)...
    # *          DB::insert('users')->values($user2)...
    # *          // Insert successful commit the changes
    # *          $db->commit();
    # *     }
    # *     catch (Database_Exception $e)
    # *     {
    # *          // Insert failed. Rolling back changes...
    # *          $db->rollback();
    # *      }
    # *
    # * @param string $mode  transaction mode
    # * @return  boolean
    # */
    def begin(self, mode):
        raise NotImplementedError("Abstract")

    #/**
    # * Commit the current transaction
    # *
    # *     // Commit the database changes
    # *     $db->commit();
    # *
    # * @return  boolean
    # */
    def commit(self):
        raise NotImplementedError("Abstract")

    #/**
    # * Abort the current transaction
    # *
    # *     // Undo the changes
    # *     $db->rollback();
    # *
    # * @return  boolean
    # */
    def rollback(self):
        raise NotImplementedError("Abstract")

    #/**
    # * Count the number of records in a table.
    # *
    # *     // Get the total number of records in the "users" table
    # *     $count = $db->count_records('users');
    # *
    # * @param   mixed    $table  table name string or array(query, alias)
    # * @return  integer
    # */
    def count_records(self, table):
        # Quote the table name
        table = self.quote_table(table)

        return self.query(minion_database_base.SELECT, 'SELECT COUNT(*) AS total_row_count FROM %s' % table, False).get('total_row_count')

    #/**
    # * Returns a normalized array describing the SQL data type
    # *
    # *     $db->datatype('char');
    # *
    # * @param   string  $type  SQL data type
    # * @return  array
    # */
#	public function datatype($type)
#	{
#		static $types = array
#		(
#			// SQL-92
#			'bit'                           => array('type' => 'string', 'exact' => TRUE),
#			'bit varying'                   => array('type' => 'string'),
#			'char'                          => array('type' => 'string', 'exact' => TRUE),
#			'char varying'                  => array('type' => 'string'),
#			'character'                     => array('type' => 'string', 'exact' => TRUE),
#			'character varying'             => array('type' => 'string'),
#			'date'                          => array('type' => 'string'),
#			'dec'                           => array('type' => 'float', 'exact' => TRUE),
#			'decimal'                       => array('type' => 'float', 'exact' => TRUE),
#			'double precision'              => array('type' => 'float'),
#			'float'                         => array('type' => 'float'),
#			'int'                           => array('type' => 'int', 'min' => '-2147483648', 'max' => '2147483647'),
#			'integer'                       => array('type' => 'int', 'min' => '-2147483648', 'max' => '2147483647'),
#			'interval'                      => array('type' => 'string'),
#			'national char'                 => array('type' => 'string', 'exact' => TRUE),
#			'national char varying'         => array('type' => 'string'),
#			'national character'            => array('type' => 'string', 'exact' => TRUE),
#			'national character varying'    => array('type' => 'string'),
#			'nchar'                         => array('type' => 'string', 'exact' => TRUE),
#			'nchar varying'                 => array('type' => 'string'),
#			'numeric'                       => array('type' => 'float', 'exact' => TRUE),
#			'real'                          => array('type' => 'float'),
#			'smallint'                      => array('type' => 'int', 'min' => '-32768', 'max' => '32767'),
#			'time'                          => array('type' => 'string'),
#			'time with time zone'           => array('type' => 'string'),
#			'timestamp'                     => array('type' => 'string'),
#			'timestamp with time zone'      => array('type' => 'string'),
#			'varchar'                       => array('type' => 'string'),
#
#			// SQL:1999
#			'binary large object'               => array('type' => 'string', 'binary' => TRUE),
#			'blob'                              => array('type' => 'string', 'binary' => TRUE),
#			'boolean'                           => array('type' => 'bool'),
#			'char large object'                 => array('type' => 'string'),
#			'character large object'            => array('type' => 'string'),
#			'clob'                              => array('type' => 'string'),
#			'national character large object'   => array('type' => 'string'),
#			'nchar large object'                => array('type' => 'string'),
#			'nclob'                             => array('type' => 'string'),
#			'time without time zone'            => array('type' => 'string'),
#			'timestamp without time zone'       => array('type' => 'string'),
#
#			// SQL:2003
#			'bigint'    => array('type' => 'int', 'min' => '-9223372036854775808', 'max' => '9223372036854775807'),
#
#			// SQL:2008
#			'binary'            => array('type' => 'string', 'binary' => TRUE, 'exact' => TRUE),
#			'binary varying'    => array('type' => 'string', 'binary' => TRUE),
#			'varbinary'         => array('type' => 'string', 'binary' => TRUE),
#		);
#
#		if (isset($types[$type]))
#			return $types[$type];
#
#		return array();
#	}

    #/**
    # * List all of the tables in the database. Optionally, a LIKE string can
    # * be used to search for specific tables.
    # *
    # *     // Get all tables in the current database
    # *     $tables = $db->list_tables();
    # *
    # *     // Get all user-related tables
    # *     $tables = $db->list_tables('user%');
    # *
    # * @param   string   $like  table to search for
    # * @return  array
    # */
    def list_tables(self, like=None):
        raise NotImplementedError("Abstract")

    #/**
    # * Lists all of the columns in a table. Optionally, a LIKE string can be
    # * used to search for specific fields.
    # *
    # *     // Get all columns from the "users" table
    # *     $columns = $db->list_columns('users');
    # *
    # *     // Get all name-related columns
    # *     $columns = $db->list_columns('users', '%name%');
    # *
    # *     // Get the columns from a table that doesn't use the table prefix
    # *     $columns = $db->list_columns('users', NULL, FALSE);
    # *
    # * @param   string  $table       table to get columns from
    # * @param   string  $like        column to search for
    # * @param   boolean $add_prefix  whether to add the table prefix automatically or not
    # * @return  array
    # */
    def list_columns(self, table, like=None, add_prefix=True):
        raise NotImplementedError("Abstract")
 
    #/**
    # * Extracts the text between parentheses, if any.
    # *
    # *     // Returns: array('CHAR', '6')
    # *     list($type, $length) = $db->_parse_type('CHAR(6)');
    # *
    # * @param   string  $type
    # * @return  array   list containing the type and length, if any
    # */
    def _parse_type(self, type):
        raise NotImplementedError("Abstract")
    
#	protected function _parse_type($type)
#	{
#		if (($open = strpos($type, '(')) === FALSE)
#		{
#			// No length specified
#			return array($type, NULL);
#		}
#
#		// Closing parenthesis
#		$close = strrpos($type, ')', $open);
#
#		// Length without parentheses
#		$length = substr($type, $open + 1, $close - 1 - $open);
#
#		// Type without the length
#		$type = substr($type, 0, $open).substr($type, $close + 1);
#
#		return array($type, $length);
#	}

    #/**
    # * Return the table prefix defined in the current configuration.
    # *
    # *     $prefix = $db->table_prefix();
    # *
    # * @return  string
    # */
    def table_prefix(self):
        return self._config['table_prefix']

    #/**
    # * Quote a value for an SQL query.
    # *
    # *     $db->quote(NULL);   // 'NULL'
    # *     $db->quote(10);     // 10
    # *     $db->quote('fred'); // 'fred'
    # *
    # * Objects passed to this function will be converted to strings.
    # * [Database_Expression] objects will be compiled.
    # * [Database_Query] objects will be compiled and converted to a sub-query.
    # * All other objects will be converted using the `__toString` method.
    # *
    # * @param   mixed   $value  any value to quote
    # * @return  string
    # * @uses    Database::escape
    # */
 
    def quote(self, value):
        from classes.minion.database.expression import database_expression

        if value is None:
            return 'NULL'
        elif value == True:
            return '1'
        elif value == False:
            return '0'
        elif isinstance(value, database_expression):
#           // Compile the expression
            return value.compile(self)
#         elif value == 
#
#		elseif (is_object($value))
#		{
#			if ($value instanceof Database_Query)
#			{
#				// Create a sub-query
#				return '('.$value->compile($this).')';
#			}
#			elseif ($value instanceof Database_Expression)
#			{
#				// Compile the expression
#				return $value->compile($this);
#			}
#			else
#			{
#				// Convert the object to a string
#				return $this->quote( (string) $value);
#			}
#		}
        elif isinstance(value, list):
            return '(%s)' % (', '.join(value))
        elif isinstance(value, int):
            return value
        elif isinstance(value, float):
            return '%F' % value

        return self.escape(value)

    #/**
    # * Quote a database column name and add the table prefix if needed.
    # *
    # *     $column = $db->quote_column($column);
    # *
    # * You can also use SQL methods within identifiers.
    # *
    # *     // The value of "column" will be quoted
    # *     $column = $db->quote_column('COUNT("column")');
    # *
    # * Objects passed to this function will be converted to strings.
    # * [Database_Expression] objects will be compiled.
    # * [Database_Query] objects will be compiled and converted to a sub-query.
    # * All other objects will be converted using the `__toString` method.
    # *
    # * @param   mixed   $column  column name or array(column, alias)
    # * @return  string
    # * @uses    Database::quote_identifier
    # * @uses    Database::table_prefix
    # */
    def quote_column(self, column):
        alias = None

        from classes.minion.database.expression import database_expression

        if isinstance(column, list):
           column, alias = column
        elif isinstance(column, database_expression):
#           // Compile the expression
            return column.compile(self)
#		if ($column instanceof Database_Query)
#		{
#			// Create a sub-query
#			$column = '('.$column->compile($this).')';
#		}
#		elseif ($column instanceof Database_Expression)
#		{
#			// Compile the expression
#			$column = $column->compile($this);
#		}
#		else
#		{
#			// Convert to a string
        column = str(column)

        if column == '*':
            return column
        elif '"' in column:
#				// Quote the column in FUNC("column") identifiers
            re.sub('/"(.+?)"/e', self.quote_column(), column)
        elif '.' in column:
            parts = column.split('.')

            prefix = self.table_prefix()

            if prefix:
#					// Get the offset of the table name, 2nd-to-last part
                offset = len(parts) - 2

#					// Add the table prefix to the table name
                parts[offset] = '%s%s' % (prefix, parts[offset])

            for part in parts:
                if part != '*':
#						// Quote each of the parts
                    part = '%s%s%s' % (self._identifier, part, self._identifier)

            column = '.'.join(parts)

        else:
            column = '%s%s%s' % (self._identifier, column, self._identifier)

        if alias:
            colimn = '%s AS %s%s%s' % (column, self._identifier, alias, self._identifier)

        return column

#	/**
#	 * Quote a database table name and adds the table prefix if needed.
#	 *
#	 *     $table = $db->quote_table($table);
#	 *
#	 * Objects passed to this function will be converted to strings.
#	 * [Database_Expression] objects will be compiled.
#	 * [Database_Query] objects will be compiled and converted to a sub-query.
#	 * All other objects will be converted using the `__toString` method.
#	 *
#	 * @param   mixed   $table  table name or array(table, alias)
#	 * @return  string
#	 * @uses    Database::quote_identifier
#	 * @uses    Database::table_prefix
#	 */
    def quote_table(self, table):
        alias = None

        from classes.minion.database.expression import database_expression

        if isinstance(table, (tuple,list)):
            table, alias = table
        elif isinstance(table, database_expression):
#           // Compile the expression
            return table.compile(self)

#		if ($table instanceof Database_Query)
#		{
#			// Create a sub-query
#			$table = '('.$table->compile($this).')'
#		}
#		elseif ($table instanceof Database_Expression)
#		{
#			// Compile the expression
#			$table = $table->compile($this);
#		}
#		else

        table = str(table)

        if '.' in table:
            parts = table.split('.')

            prefix = self.table_prefix()

            if prefix:
#					// Get the offset of the table name, last part
                offset = len(parts) - 1

#					// Add the table prefix to the table name
                parts[offset] = '%s%s' % (prefix, parts[offset])

#					// Quote each of the parts
            parts = ['%s%s%s' % (self._identifier, p, self._identifier) for p in parts]

            table = '.'.join(parts)
        else:
#				// Add the table prefix
            table = '%s%s%s%s' % (self._identifier, self.table_prefix(), table, self._identifier)

        if alias:
            table = '%s AS %s%s%s%s' % (table, self._identifier, self.table_prefix(), alias, self._identifier)

        return table
#
#	/**
#	 * Quote a database identifier
#	 *
#	 * Objects passed to this function will be converted to strings.
#	 * [Database_Expression] objects will be compiled.
#	 * [Database_Query] objects will be compiled and converted to a sub-query.
#	 * All other objects will be converted using the `__toString` method.
#	 *
#	 * @param   mixed   $value  any identifier
#	 * @return  string
#	 */
#	public function quote_identifier($value)
#	{
#		if (is_array($value))
#		{
#			list($value, $alias) = $value;
#		}
#
#		if ($value instanceof Database_Query)
#		{
#			// Create a sub-query
#			$value = '('.$value->compile($this).')';
#		}
#		elseif ($value instanceof Database_Expression)
#		{
#			// Compile the expression
#			$value = $value->compile($this);
#		}
#		else
#		{
#			// Convert to a string
#			$value = (string) $value;
#
#			if (strpos($value, '.') !== FALSE)
#			{
#				$parts = explode('.', $value);
#
#				foreach ($parts as & $part)
#				{
#					// Quote each of the parts
#					$part = $this->_identifier.$part.$this->_identifier;
#				}
#
#				$value = implode('.', $parts);
#			}
#			else
#			{
#				$value = $this->_identifier.$value.$this->_identifier;
#			}
#		}
#
#		if (isset($alias))
#		{
#			$value .= ' AS '.$this->_identifier.$alias.$this->_identifier;
#		}
#
#		return $value;
#	}
#
#	/**
#	 * Sanitize a string by escaping characters that could cause an SQL
#	 * injection attack.
#	 *
#	 *     $value = $db->escape('any string');
#	 *
#	 * @param   string   $value  value to quote
#	 * @return  string
#	 */

    def escape(self, value):
        raise NotImplementedError("Abstract")

