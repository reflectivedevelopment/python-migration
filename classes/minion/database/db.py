
#	/**
#	 * Create a new [Database_Query] of the given type.
#	 *
#	 *     // Create a new SELECT query
#	 *     $query = DB::query(Database::SELECT, 'SELECT * FROM users');
#	 *
#	 *     // Create a new DELETE query
#	 *     $query = DB::query(Database::DELETE, 'DELETE FROM users WHERE id = 5');
#	 *
#	 * Specifying the type changes the returned result. When using
#	 * `Database::SELECT`, a [Database_Query_Result] will be returned.
#	 * `Database::INSERT` queries will return the insert id and number of rows.
#	 * For all other queries, the number of affected rows is returned.
#	 *
#	 * @param   integer  $type  type: Database::SELECT, Database::UPDATE, etc
#	 * @param   string   $sql   SQL statement
#	 * @return  Database_Query
#	 */
#	public static function query($type, $sql)
#	{
#		return new Database_Query($type, $sql);
#	}
#
#
    # /**
    # * Create a new [Database_Query_Builder_Select]. Each argument will be
    # * treated as a column. To generate a `foo AS bar` alias, use an array.
    # *
    # *     // SELECT id, username
    # *     $query = DB::select('id', 'username');
    # *
    # *     // SELECT id AS user_id
    # *     $query = DB::select(array('id', 'user_id'));
    # *
    # * @param   mixed   $columns  column name or array($column, $alias) or object
    # * @return  Database_Query_Builder_Select
    # */
def select(columns=None):
    from classes.minion.database.query.builder.select import database_query_builder_select
    return database_query_builder_select(columns)

#/**
#	 * Create a new [Database_Query_Builder_Select] from an array of columns.
#	 *
#	 *     // SELECT id, username
#	 *     $query = DB::select_array(array('id', 'username'));
#	 *
#	 * @param   array   $columns  columns to select
#	 * @return  Database_Query_Builder_Select
#	 */
#	public static function select_array(array $columns = NULL)
#	{
#		return new Database_Query_Builder_Select($columns);
#	}
#
#	/**
#	 * Create a new [Database_Query_Builder_Insert].
#	 *
#	 *     // INSERT INTO users (id, username)
#	 *     $query = DB::insert('users', array('id', 'username'));
#	 *
#	 * @param   string  $table    table to insert into
#	 * @param   array   $columns  list of column names or array($column, $alias) or object
#	 * @return  Database_Query_Builder_Insert
#	 */
def insert(table=None, columns=None):
    from classes.minion.database.query.builder.insert import database_query_builder_insert
    return database_query_builder_insert(table, columns)

#	/**
#	 * Create a new [Database_Query_Builder_Update].
#	 *
#	 *     // UPDATE users
#	 *     $query = DB::update('users');
#	 *
#	 * @param   string  $table  table to update
#	 * @return  Database_Query_Builder_Update
#	 */
def update(table=None):
    from classes.minion.database.query.builder.update import database_query_builder_update
    return database_query_builder_update(table)

#	/**
#	 * Create a new [Database_Query_Builder_Delete].
#	 *
#	 *     // DELETE FROM users
#	 *     $query = DB::delete('users');
#	 *
#	 * @param   string  $table  table to delete from
#	 * @return  Database_Query_Builder_Delete
#	 */
def delete(table=None):
    from classes.minion.database.query.builder.delete import database_query_builder_delete
    return database_query_builder_delete(table)

#	/**
#	 * Create a new [Database_Expression] which is not escaped. An expression
#	 * is the only way to use SQL functions within query builders.
#	 *
#	 *     $expression = DB::expr('COUNT(users.id)');
#	 *     $query = DB::update('users')->set(array('login_count' => DB::expr('login_count + 1')))->where('id', '=', $id);
#	 *     $users = ORM::factory('user')->where(DB::expr("BINARY `hash`"), '=', $hash)->find();
#	 *
#	 * @param   string  $string  expression
#	 * @param   array   parameters
#	 * @return  Database_Expression
#	 */
#	public static function expr($string, $parameters = array())
#	{
#		return new Database_Expression($string, $parameters);
#	}
#
#} // End DB
