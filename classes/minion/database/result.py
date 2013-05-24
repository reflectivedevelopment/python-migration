#/**
# * Database result wrapper.  See [Results](/database/results) for usage and examples.
# *
# */

class database_result():
#abstract class Kohana_Database_Result implements Countable, Iterator, SeekableIterator, ArrayAccess {

#	// Executed SQL for this result
    _query = None

#	// Raw result resource
    _result = None

#	// Total number of rows and current row
    _total_rows  = 0
    _current_row = 0

#	// Return rows as an object or associative array
    _as_object = None

#	// Parameters for __construct when using object results
    _object_params = None;

#	/**
#	 * Sets the total number of rows and stores the result locally.
#	 *
#	 * @param   mixed   $result     query result
#	 * @param   string  $sql        SQL query
#	 * @param   mixed   $as_object
#	 * @param   array   $params
#	 * @return  void
#	 */
    def __init__(self, result, sql, as_object = None, params = None):
	#// Store the result locally
        self._result = result

	#// Store the SQL locally
	self._query = sql

        if as_object is not None:
            self._as_object = as_object

        if params is not None:
            #// Object constructor params
            self._object_params = params

    def __len__(self):
        return self._total_rows

#	/**
#	 * Return all of the rows in the result as an array.
#	 *
#	 *     // Indexed array of all rows
#	 *     $rows = $result->as_array();
#	 *
#	 *     // Associative array of rows by "id"
#	 *     $rows = $result->as_array('id');
#	 *
#	 *     // Associative array of rows, "id" => "name"
#	 *     $rows = $result->as_array('id', 'name');
#	 *
#	 * @param   string  $key    column for associative keys
#	 * @param   string  $value  column for values
#	 * @return  array
#	 */
    def as_array(self, key = None, value = None):
        results = []

        if key is None and value is None:
            return self._result

        elif key is None:
            for row in self._result:
                result.append(row[value])

        elif value is None:
            result = dict()

            for row in self._result:
                result[row[key]] = row

            return result
        else:
            result = dict()

            for row in self._result:
                result[row[key]] = row[value]

            return result

