from classes.minion.database.query.builder import database_query_builder

#/**
# * Database query builder for WHERE statements. See [Query Builder](/database/query/builder) for usage and examples.
# */
class database_query_builder_where(database_query_builder):

    def __init__(self, type=None, sql=''):
        # // WHERE ...
        self._where = []
  
        # // ORDER BY ...
        self._order_by = []

        # // LIMIT ...
        self._limit = None

        database_query_builder.__init__(self, type, sql)
#
#	/**
#	 * Alias of and_where()
#	 *
#	 * @param   mixed   $column  column name or array($column, $alias) or object
#	 * @param   string  $op      logic operator
#	 * @param   mixed   $value   column value
#	 * @return  $this
#	 */
    def where(self, column, op, value):
        return self.and_where(column, op, value)

#	/**
#	 * Creates a new "AND WHERE" condition for the query.
#	 *
#	 * @param   mixed   $column  column name or array($column, $alias) or object
#	 * @param   string  $op      logic operator
#	 * @param   mixed   $value   column value
#	 * @return  $this
#	 */
    def and_where(self, column, op, value):
        self._where.append( {'AND': [column, op, value]} )

        return self

#	/**
#	 * Creates a new "OR WHERE" condition for the query.
#	 *
#	 * @param   mixed   $column  column name or array($column, $alias) or object
#	 * @param   string  $op      logic operator
#	 * @param   mixed   $value   column value
#	 * @return  $this
#	 */
    def or_where(self, column, op, value):
        self._where.append( {'OR': [column, op, value]} )

        return self

#	/**
#	 * Alias of and_where_open()
#	 *
#	 * @return  $this
#	 */
    def where_open(self):
        return self.and_where_open()

#	/**
#	 * Opens a new "AND WHERE (...)" grouping.
#	 *
#	 * @return  $this
#	 */
    def and_where_open(self):
        self._where.append({'AND': '('})

        return self

#	/**
#	 * Opens a new "OR WHERE (...)" grouping.
#	 *
#	 * @return  $this
#	 */
    def or_where_open(self):
        self._where.append( {'OR': '('} )

        return self

#	/**
#	 * Closes an open "AND WHERE (...)" grouping.
#	 *
#	 * @return  $this
#	 */
    def where_close(self):
        return self.and_where_close()

#	/**
#	 * Closes an open "AND WHERE (...)" grouping.
#	 *
#	 * @return  $this
#	 */
    def and_where_close(self):
        self._where.append({'AND': ')'})

        return self

#	/**
#	 * Closes an open "OR WHERE (...)" grouping.
#	 *
#	 * @return  $this
#	 */
    def or_where_close(self):
        self._where.append({'OR': ')'})

        return self

#	/**
#	 * Applies sorting with "ORDER BY ..."
#	 *
#	 * @param   mixed   $column     column name or array($column, $alias) or object
#	 * @param   string  $direction  direction of sorting
#	 * @return  $this
#	 */
    def order_by(self, column, direction = None):
        self._order_by.append([column, direction])

        return self

#	/**
#	 * Return up to "LIMIT ..." results
#	 *
#	 * @param   integer  $number  maximum results to return or NULL to reset
#	 * @return  $this
#	 */
    def limit(self, number):
        self._limit = number

        return self

