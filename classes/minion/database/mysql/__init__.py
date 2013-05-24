from ..base import minion_database_base
import hashlib
import sqlalchemy
from result import database_mysql_result

def instance(name=None, config=None):
    return minion_database_mysql(name=name, config=config)

# Makes use of sqlalchemy

class minion_database_mysql(minion_database_base):

    # Database in use by each connection
    _current_databases = dict()

    # use SET NAMES to set the character set
    _set_names = None

    # Idenetifier for this connection within the python driver
    _connection_id = None

    # Identify the charset
    _charset = None

    # MySQL uses a backtick for identifiers
    _identifier = '`'

    def connect(self):
        if self._connection is not None:
            return

#        if minion_database_sqlalchemy._set_names is None:
#            
#		if (Database_MySQL::$_set_names === NULL)
#		{
#			// Determine if we can use mysql_set_charset(), which is only
#			// available on PHP 5.2.3+ when compiled against MySQL 5.0+
#			Database_MySQL::$_set_names = ! function_exists('mysql_set_charset');
#		}

        database = self._config['database']
        hostname = self._config['hostname']
        username = self._config['username']
        password = self._config['password']
        persistent = self._config['persistent']

#		// Prevent this information from showing up in traces
#		unset($this->_config['connection']['username'], $this->_config['connection']['password']);

#'mysql://root:@localhost/test'
        try:
            self._connection = sqlalchemy.create_engine('mysql://%s:%s@%s/%s' % (username, password, hostname, database), echo=False)
        except Exception as e:
            self._connection = None

            raise Exception ('Connection failed: %s' % e)

	#// \xFF is a better delimiter, but the Python driver uses underscore
        self._connection_id = hashlib.sha1('%s_%s_%s' % (hostname, username, password))

        if self._charset is not None:
            pass
#          	if ( ! empty($this->_config['charset']))
#		{
#			// Set the character set
#			$this->set_charset($this->_config['charset']);
#		}

#		if ( ! empty($this->_config['connection']['variables']))
#		{
#			// Set session variables
#			$variables = array();
#
#			foreach ($this->_config['connection']['variables'] as $var => $val)
#			{
#				$variables[] = 'SESSION '.$var.' = '.$this->quote($val);
#			}
#
#			mysql_query('SET '.implode(', ', $variables), $this->_connection);
#		}
#	}

    def disconnect(self):
        status = True

        try:
            if self.connection is not None:
                self._connection.close()

                self._connection = None

                super(self).disconnect()
        except Exception as e:
            # Database is probablay not disconnected
#            status = not ??
#			$status = ! is_resource($this->_connection);
            raise Exception("Can't handle exception!")
        return status;

    def set_charset(self, charset):
        raise NotImplementedError("TODO")
    
#	public function set_charset($charset)
#	{
#		// Make sure the database is connected
#		$this->_connection or $this->connect();
#
#		if (Database_MySQL::$_set_names === TRUE)
#		{
#			// PHP is compiled against MySQL 4.x
#			$status = (bool) mysql_query('SET NAMES '.$this->quote($charset), $this->_connection);
#		}
#		else
#		{
#			// PHP is compiled against MySQL 5.x
#			$status = mysql_set_charset($charset, $this->_connection);
#		}
#
#		if ($status === FALSE)
#		{
#			throw new Database_Exception(':error',
#				array(':error' => mysql_error($this->_connection)),
#				mysql_errno($this->_connection));
#		}
#	}

    def query(self, type, sql, as_object = False, params = None):
        if not self._connection:
            self.connect()

	#	if ( ! empty($this->_config['profiling']))
	#	{
	#		// Benchmark this query for the current instance
	#		$benchmark = Profiler::start("Database ({$this->_instance})", $sql);
	#	}

	#	if ( ! empty($this->_config['connection']['persistent']) AND $this->_config['connection']['database'] !== Database_MySQL::$_current_databases[$this->_connection_id])
	#	{
	#		// Select database on persistent connections
	#		$this->_select_db($this->_config['connection']['database']);
	#	}

        result = self._connection.execute(sql)
#		// Execute the query
#		if (($result = mysql_query($sql, $this->_connection)) === FALSE)
#		{
#			if (isset($benchmark))
#			{
#				// This benchmark is worthless
#				Profiler::delete($benchmark);
#			}
#
#			throw new Database_Exception(':error [ :query ]',
#				array(':error' => mysql_error($this->_connection), ':query' => $sql),
#				mysql_errno($this->_connection));
#		}

	#	if (isset($benchmark))
	#	{
	#		Profiler::stop($benchmark);
	#	}

        # set the last query
        self.last_query = sql

        if type == minion_database_base.SELECT:
            return database_mysql_result(result, sql)
        elif type == minion_database_base.INSERT:
            return (result.lastrowid, result.rowcount)
        else:
            return result.rowcount

#	public function datatype($type)
#	{
#		static $types = array
#		(
#			'blob'                      => array('type' => 'string', 'binary' => TRUE, 'character_maximum_length' => '65535'),
#			'bool'                      => array('type' => 'bool'),
#			'bigint unsigned'           => array('type' => 'int', 'min' => '0', 'max' => '18446744073709551615'),
#			'datetime'                  => array('type' => 'string'),
#			'decimal unsigned'          => array('type' => 'float', 'exact' => TRUE, 'min' => '0'),
#			'double'                    => array('type' => 'float'),
#			'double precision unsigned' => array('type' => 'float', 'min' => '0'),
#			'double unsigned'           => array('type' => 'float', 'min' => '0'),
#			'enum'                      => array('type' => 'string'),
#			'fixed'                     => array('type' => 'float', 'exact' => TRUE),
#			'fixed unsigned'            => array('type' => 'float', 'exact' => TRUE, 'min' => '0'),
#			'float unsigned'            => array('type' => 'float', 'min' => '0'),
#			'int unsigned'              => array('type' => 'int', 'min' => '0', 'max' => '4294967295'),
#			'integer unsigned'          => array('type' => 'int', 'min' => '0', 'max' => '4294967295'),
#			'longblob'                  => array('type' => 'string', 'binary' => TRUE, 'character_maximum_length' => '4294967295'),
#			'longtext'                  => array('type' => 'string', 'character_maximum_length' => '4294967295'),
#			'mediumblob'                => array('type' => 'string', 'binary' => TRUE, 'character_maximum_length' => '16777215'),
#			'mediumint'                 => array('type' => 'int', 'min' => '-8388608', 'max' => '8388607'),
#			'mediumint unsigned'        => array('type' => 'int', 'min' => '0', 'max' => '16777215'),
#			'mediumtext'                => array('type' => 'string', 'character_maximum_length' => '16777215'),
#			'national varchar'          => array('type' => 'string'),
#			'numeric unsigned'          => array('type' => 'float', 'exact' => TRUE, 'min' => '0'),
#			'nvarchar'                  => array('type' => 'string'),
#			'point'                     => array('type' => 'string', 'binary' => TRUE),
#			'real unsigned'             => array('type' => 'float', 'min' => '0'),
#			'set'                       => array('type' => 'string'),
#			'smallint unsigned'         => array('type' => 'int', 'min' => '0', 'max' => '65535'),
#			'text'                      => array('type' => 'string', 'character_maximum_length' => '65535'),
#			'tinyblob'                  => array('type' => 'string', 'binary' => TRUE, 'character_maximum_length' => '255'),
#			'tinyint'                   => array('type' => 'int', 'min' => '-128', 'max' => '127'),
#			'tinyint unsigned'          => array('type' => 'int', 'min' => '0', 'max' => '255'),
#			'tinytext'                  => array('type' => 'string', 'character_maximum_length' => '255'),
#			'year'                      => array('type' => 'string'),
#		);
#
#		$type = str_replace(' zerofill', '', $type);
#
#		if (isset($types[$type]))
#			return $types[$type];
#
#		return parent::datatype($type);
#	}

    #/**
    # * Start a SQL transaction
    # *
    # * @link http://dev.mysql.com/doc/refman/5.0/en/set-transaction.html
    # *
    # * @param string $mode  Isolation level
    # * @return boolean
    # */
    def begin(self, mode = None):
        raise NotImplementedError("TODO")
#	public function begin($mode = NULL)
#	{
#		// Make sure the database is connected
#		$this->_connection or $this->connect();
#
#		if ($mode AND ! mysql_query("SET TRANSACTION ISOLATION LEVEL $mode", $this->_connection))
#		{
#			throw new Database_Exception(':error',
#				array(':error' => mysql_error($this->_connection)),
#				mysql_errno($this->_connection));
#		}
#
#		return (bool) mysql_query('START TRANSACTION', $this->_connection);
#	}

#/**
# * Commit a SQL transaction
# *
# * @return boolean
# */
    def commit(self):
        raise NotImplementedError("TODO")
#	public function commit()
#	{
#		// Make sure the database is connected
#		$this->_connection or $this->connect();
#
#		return (bool) mysql_query('COMMIT', $this->_connection);
#	}

#/**
# * Rollback a SQL transaction
# *
# * @return boolean
# */
    def rollback(self):
        raise NotImplementedError("TODO")
#	public function rollback()
#	{
#		// Make sure the database is connected
#		$this->_connection or $this->connect();
#
#		return (bool) mysql_query('ROLLBACK', $this->_connection);
#	}

    def list_tables(self, like=None):
        raise NotImplementedError("TODO")
#	public function list_tables($like = NULL)
#	{
#		if (is_string($like))
#		{
#			// Search for table names
#			$result = $this->query(Database::SELECT, 'SHOW TABLES LIKE '.$this->quote($like), FALSE);
#		}
#		else
#		{
#			// Find all table names
#			$result = $this->query(Database::SELECT, 'SHOW TABLES', FALSE);
#		}
#
#		$tables = array();
#		foreach ($result as $row)
#		{
#			$tables[] = reset($row);
#		}
#
#		return $tables;
#	}

    def list_columns(self, table, like=None, add_prefix=True):
        raise NotImplementedError("TODO")
#	public function list_columns($table, $like = NULL, $add_prefix = TRUE)
#	{
#		// Quote the table name
#		$table = ($add_prefix === TRUE) ? $this->quote_table($table) : $table;
#
#		if (is_string($like))
#		{
#			// Search for column names
#			$result = $this->query(Database::SELECT, 'SHOW FULL COLUMNS FROM '.$table.' LIKE '.$this->quote($like), FALSE);
#		}
#		else
#		{
#			// Find all column names
#			$result = $this->query(Database::SELECT, 'SHOW FULL COLUMNS FROM '.$table, FALSE);
#		}
#
#		$count = 0;
#		$columns = array();
#		foreach ($result as $row)
#		{
#			list($type, $length) = $this->_parse_type($row['Type']);
#
#			$column = $this->datatype($type);
#
#			$column['column_name']      = $row['Field'];
#			$column['column_default']   = $row['Default'];
#			$column['data_type']        = $type;
#			$column['is_nullable']      = ($row['Null'] == 'YES');
#			$column['ordinal_position'] = ++$count;
#
#			switch ($column['type'])
#			{
#				case 'float':
#					if (isset($length))
#					{
#						list($column['numeric_precision'], $column['numeric_scale']) = explode(',', $length);
#					}
#				break;
#				case 'int':
#					if (isset($length))
#					{
#						// MySQL attribute
#						$column['display'] = $length;
#					}
#				break;
#				case 'string':
#					switch ($column['data_type'])
#					{
#						case 'binary':
#						case 'varbinary':
#							$column['character_maximum_length'] = $length;
#						break;
#						case 'char':
#						case 'varchar':
#							$column['character_maximum_length'] = $length;
#						case 'text':
#						case 'tinytext':
#						case 'mediumtext':
#						case 'longtext':
#							$column['collation_name'] = $row['Collation'];
#						break;
#						case 'enum':
#						case 'set':
#							$column['collation_name'] = $row['Collation'];
#							$column['options'] = explode('\',\'', substr($length, 1, -1));
#						break;
#					}
#				break;
#			}
#
#			// MySQL attributes
#			$column['comment']      = $row['Comment'];
#			$column['extra']        = $row['Extra'];
#			$column['key']          = $row['Key'];
#			$column['privileges']   = $row['Privileges'];
#
#			$columns[$row['Field']] = $column;
#		}
#
#		return $columns;
#	}

    def escape(self, value):
        raise NotImplementedError("TODO")
        
#	public function escape($value)
#	{
#		// Make sure the database is connected
#		$this->_connection or $this->connect();
#
#		if (($value = mysql_real_escape_string( (string) $value, $this->_connection)) === FALSE)
#		{
#			throw new Database_Exception(':error',
#				array(':error' => mysql_error($this->_connection)),
#				mysql_errno($this->_connection));
#		}
#
#		// SQL standard is to use single-quotes for all values
#		return "'$value'";
#	}
#
#} // End Database_MySQL
