from classes.minion.database import base

#<?php defined('SYSPATH') OR die('No direct script access.');
#/**
# * Database expressions can be used to add unescaped SQL fragments to a
# * [Database_Query_Builder] object.
# *
# * For example, you can use an expression to generate a column alias:
# *
# *     // SELECT CONCAT(first_name, last_name) AS full_name
# *     $query = DB::select(array(DB::expr('CONCAT(first_name, last_name)'), 'full_name')));
# *
# * More examples are available on the [Query Builder](database/query/builder#database-expressions) page
# * 
# */

import re

def strtr(s, repl):
    pattern = '|'.join(map(re.escape, sorted(repl, key=len, reverse=True)))
    return re.sub(pattern, lambda m: repl[m.group()], s)


class database_expression():
#	// Unquoted parameters
    _parameters = None

#	// Raw expression string
    _value = None

#	/**
#	 * Sets the expression string.
#	 *
#	 *     $expression = new Database_Expression('COUNT(users.id)');
#	 *
#	 * @param   string  $value      raw SQL expression string
#	 * @param   array   $parameters unquoted parameter values
#	 * @return  void
#	 */
    def __init__(self, value, parameters = []):
#		// Set the expression string
        self._value = value
        self._parameters = parameters

#	/**
#	 * Bind a variable to a parameter.
#	 *
#	 * @param   string  $param  parameter key to replace
#	 * @param   mixed   $var    variable to use
#	 * @return  $this
#	 */
#	public function bind($param, & $var)
#	{
#		$this->_parameters[$param] =& $var;
#
#		return $this;
#	}
#
#	/**
#	 * Set the value of a parameter.
#	 *
#	 * @param   string  $param  parameter key to replace
#	 * @param   mixed   $value  value to use
#	 * @return  $this
#	 */
    def param(self, param, value):
        self._parameters[param] = value

        return self

#	/**
#	 * Add multiple parameter values.
#	 *
#	 * @param   array   $params list of parameter values
#	 * @return  $this
#	 */
    def parameters(self, params):
        self._parameters = dict(params.items() + self._parameters.items())

        return self

#	/**
#	 * Get the expression value as a string.
#	 *
#	 *     $sql = $expression->value();
#	 *
#	 * @return  string
#	 */
    def value(self):
        return str(self._value)

#	/**
#	 * Return the value of the expression as a string.
#	 *
#	 *     echo $expression;
#	 *
#	 * @return  string
#	 * @uses    Database_Expression::value
#	 */
#	public function __toString()
#	{
#		return $this->value();
#	}
#
#	/**
#	 * Compile the SQL expression and return it. Replaces any parameters with
#	 * their given values.
#	 *
#	 * @param   mixed    Database instance or name of instance
#	 * @return  string
#	 */
    def compile(self, db = None):
        if not isinstance(db, (base.minion_database_base)):
#			// Get the database instance
            db = base.instance(db)
        value = self.value()

        if len(self._parameters) > 0:
#			// Quote all of the parameter values
            params = dict()

            for key in self._parameters:
                params[key] = db.quote(self._parameters[key])

            value = strtr(value, params)
            
        return value
