from classes.minion.database.query import database_query

#/**
# * Database query builder. See [Query Builder](/database/query/builder) for usage and examples.
# *
# */
class database_query_builder(database_query):
#	/**
#	 * Compiles an array of JOIN statements into an SQL partial.
#	 *
#	 * @param   object  $db     Database instance
#	 * @param   array   $joins  join statements
#	 * @return  string
#	 */
    def _compile_join(self, db, joins):
        statements = []

        for join in joins:
            statements.append(join.compile(db))

        return ' '.join(statements)

#	/**
#	 * Compiles an array of conditions into an SQL partial. Used for WHERE
#	 * and HAVING.
#	 *
#	 * @param   object  $db          Database instance
#	 * @param   array   $conditions  condition statements
#	 * @return  string
#	 */
    def _compile_conditions(self, db, conditions):
        last_condition = None

        sql = '';

        for group in conditions:
            logic = None
            condition = None
            for logic, condition in group.iteritems():
                if condition == '(':
                    if len(sql) > 0 and last_condition != '(':
                        sql = '%s %s ' % (sql, logic)
                    sql = '%s(' % sql
                elif condition == ')':
                    sql = '%s)' % sql
                else:
                    if len(sql) > 0 and last_condition != '(':
                        sql = '%s %s ' % (sql, logic)

                    column, op, value = condition

                    if value is None:
                        if op == '=':
                            op = 'IS'
                        elif op == '!=':
                            op = 'IS NOT'

#					// Database operators are always uppercase
                    op = op.upper()

                    if op == 'BETWEEN' and isinstance(value, (list,tuple)):

#						// BETWEEN always has exactly two arguments
                        (min,max) = value

                        if isinstance(min, str) and not self._parameters.has_key(min):
#							// Quote the value, it is not a parameter
                            min = db.quote(min) 

                        if isinstance(max, str) and not self._parameters.has_key(max):
#							// Quote the value, it is not a parameter
                            max = db.quote(max) 

#						// Quote the min and max value
                        value = '%s AND %s' % (min, max)

                    elif isinstance(value, str) and not self._parameters.has_key(value):
#						// Quote the value, it is not a parameter
                        value = db.quote(value)

                    if column is not None:
                        if isinstance(column, (list, tuple)):
#							// Use the column name
                            column = db.quote_identifier(column[0])
                        else:
#							// Apply proper quoting to the column
                            column = db.quote_column(column)
#
                    last_condition = condition
#
        return sql

#	/**
#	 * Compiles an array of set values into an SQL partial. Used for UPDATE.
#	 *
#	 * @param   object  $db      Database instance
#	 * @param   array   $values  updated values
#	 * @return  string
#	 */
    def _compile_set(self, db, values):
        set = dict()

        for group in values:
            # Split the set
            (column, value) = group

            # Quote the column name
            column = db.quote_column(column)

            if isinstance(value, str) and not self._parameters.has_key(value):
                # Quote the value, it is not a parameter
                value = db.quote(value)

            set[column] = '%s = %s' % (column, value)

        return ', '.join(set.values())

#	/**
#	 * Compiles an array of GROUP BY columns into an SQL partial.
#	 *
#	 * @param   object  $db       Database instance
#	 * @param   array   $columns
#	 * @return  string
#	 */
    def _compile_group_by(self, db, columns):
        group = []

        for column in columns:
            if isinstance(column, (list,tuple)):
#				// Use the column alias
                column = db.quote_identifier(end(column[-1]))
            else:
#				// Apply proper quoting to the column
                column = db.quote_column(column)

            group.append(column)

        return 'GROUP BY %s' % (', '.join(group))

#	/**
#	 * Compiles an array of ORDER BY statements into an SQL partial.
#	 *
#	 * @param   object  $db       Database instance
#	 * @param   array   $columns  sorting columns
#	 * @return  string
#	 */
    def _compile_order_by(self, db, columns):
        sort = []

        for group in columns:
            column, direction = group

            if isinstance(column, (list,tuple)):
                # use the column alias
                column = db.quote_identifier(column[-1])
            else:
                # apply proper quoting to the column
                column = db.quote_column(column)

            if direction:
                # Make the direction uppercase
                direction = (' %s' % direction).upper()
            else:
                direction = ''

            sort.append('%s%s' % (column, direction))

        return 'ORDER BY %s' % (', '.join(sort))

#	/**
#	 * Reset the current builder status.
#	 *
#	 * @return  $this
#	 */
    def reset(self):
        raise NotImplementedError("Abstract")

