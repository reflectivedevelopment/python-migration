#/**
# * Database query wrapper.  See [Parameterized Statements](database/query/parameterized) for usage and examples.
# */
import re

def strtr(s, repl):
    pattern = '|'.join(map(re.escape, sorted(repl, key=len, reverse=True)))
    return re.sub(pattern, lambda m: repl[m.group()], s)

class database_query():

#	// Query type
    _type = None;

#	// SQL statement
    _sql = None;

#	// Quoted query parameters
    _parameters = dict();

#	// Return results as associative arrays or objects
    _as_object = False;

#	// Parameters for __construct when using object results
    _object_params = [];

#	/**
#	 * Creates a new SQL query of the specified type.
#	 *
#	 * @param   integer  $type  query type: Database::SELECT, Database::INSERT, etc
#	 * @param   string   $sql   query string
#	 * @return  void
#	 */
    def __init__(self, type, sql):
        self._type = type
        self._sql = sql

#	/**
#	 * Return the SQL query string.
#	 *
#	 * @return  string
#	 */
#	final public function __toString()
#	{
#		try
#		{
#			// Return the SQL string
#			return $this->compile(Database::instance());
#		}
#		catch (Exception $e)
#		{
#			return Kohana_Exception::text($e);
#		}
#	}

#	/**
#	 * Get the type of the query.
#	 *
#	 * @return  integer
#	 */
    def type(self):
        return self._type

#	/**
#	 * Enables the query to be cached for a specified amount of time.
#	 *
#	 * @param   integer  $lifetime  number of seconds to cache, 0 deletes it from the cache
#	 * @param   boolean  whether or not to execute the query during a cache hit
#	 * @return  $this
#	 * @uses    Kohana::$cache_life
#	 */
#	public function cached($lifetime = NULL, $force = FALSE)
#	{
#		if ($lifetime === NULL)
#		{
#			// Use the global setting
#			$lifetime = Kohana::$cache_life;
#		}
#
#		$this->_force_execute = $force;
#		$this->_lifetime = $lifetime;
#
#		return $this;
#	}

#	/**
#	 * Returns results as associative arrays
#	 *
#	 * @return  $this
#	 */
#	public function as_assoc()
#	{
#		$this->_as_object = FALSE;
#
#		$this->_object_params = array();
#
#		return $this;
#	}

#	/**
#	 * Returns results as objects
#	 *
#	 * @param   string  $class  classname or TRUE for stdClass
#	 * @param   array   $params
#	 * @return  $this
#	 */
#	public function as_object($class = TRUE, array $params = NULL)
#	{
#		$this->_as_object = $class;
#
#		if ($params)
#		{
#			// Add object parameters
#			$this->_object_params = $params;
#		}
#
#		return $this;
#	}

#	/**
#	 * Set the value of a parameter in the query.
#	 *
#	 * @param   string   $param  parameter key to replace
#	 * @param   mixed    $value  value to use
#	 * @return  $this
#	 */
    def param(self, param, val):
        self._parameters[param] = val

        return self

#	public function bind($param, & $var)
#	{
#		// Bind a value to a variable
#		$this->_parameters[$param] =& $var;
#
#		return $this;
#	}

#	/**
#	 * Add multiple parameters to the query.
#	 *
#	 * @param   array  $params  list of parameters
#	 * @return  $this
#	 */
    def parameters(self, params):
        # Merge new parameters in 
        self._parameters.update(params)

        return self



#	/**
#	 * Compile the SQL query and return it. Replaces any parameters with their
#	 * given values.
#	 *
#	 * @param   object  $db  Database instance
#	 * @return  string
#	 */
    def compile(self, db):
        # Import the SQL locally
        sql = self._sql

        if len(self._parameters) > 0:
            values = dict()

            for key in self._parameters.keys():
                values[key] = db.quote(self._parameters[key])

            sql = strtr(sql, values)

        return sql

#	/**
#	 * Execute the current query on the given database.
#	 *
#	 * @param   mixed    $db  Database instance or name of instance
#	 * @param   string   result object classname, TRUE for stdClass or FALSE for array
#	 * @param   array    result object constructor arguments
#	 * @return  object   Database_Result for SELECT queries
#	 * @return  mixed    the insert id for INSERT queries
#	 * @return  integer  number of affected rows for all other queries
#	 */
    def execute(self, db=None, as_object=None, object_params=None):
#		if ( ! is_object($db))
#		{
#			// Get the database instance
#			$db = Database::instance($db);
#		}

#		if ($as_object === NULL)
#		{
#			$as_object = $this->_as_object;
#		}

#		if ($object_params === NULL)
#		{
#			$object_params = $this->_object_params;
#		}

#		// Compile the SQL query
        sql = self.compile(db)

#		if ($this->_lifetime !== NULL AND $this->_type === Database::SELECT)
#		{
#			// Set the cache key based on the database instance name and SQL
#			$cache_key = 'Database::query("'.$db.'", "'.$sql.'")';
#
#			// Read the cache first to delete a possible hit with lifetime <= 0
#			if (($result = Kohana::cache($cache_key, NULL, $this->_lifetime)) !== NULL
#				AND ! $this->_force_execute)
#			{
#				// Return a cached result
#				return new Database_Result_Cached($result, $sql, $as_object, $object_params);
#			}
#		}
#
#		// Execute the query
        result = db.query(self._type, sql, as_object, object_params)
#
#		if (isset($cache_key) AND $this->_lifetime > 0)
#		{
#			// Cache the result array
#			Kohana::cache($cache_key, $result->as_array(), $this->_lifetime);
#		}
#
        return result
#		return $result;
#	}
#
#} // End Database_Query
