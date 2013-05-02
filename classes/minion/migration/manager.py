from classes.model.minion.migration import model_minion_migration as migration_model
from classes.minion.migration.database import faux_instance
from classes.minion.database.mysql import minion_database_mysql as database

#/**
# * The migration manager is responsible for locating migration files, syncing
# * them with the migrations table in the database and selecting any migrations
# * that need to be executed in order to reach a target version
# *
# * @author Matt Button <matthew@sigswitch.com>
# */

class minion_migration_manager():

    #/**
    # * The database connection that sould be used
    # * @var Kohana_Database
    # */
    _db = None

    #/**
    # * Model used to interact with the migrations table in the database
    # * @var Model_Minion_Migration
    # */
    _model = None

    #/**
    # * Whether this is a dry run migration
    # * @var boolean
    # */
    _dry_run = False

    #/**
    # * A set of SQL queries that were generated on the dry run
    # * @var array
    # */
    _dry_run_sql = {}

    #/**
    # * Set of migrations that were executed
    # */
    _executed_migrations = {}

    #/**
    # * Constructs the object, allows injection of a Database connection
    # *
    # * @param Kohana_Database        The database connection that should be passed to migrations
    # * @param Model_Minion_Migration Inject an instance of the minion model into the manager
    # */
    def __init__(self, db, model=None):
        if model is None:
            model = migration_model(db)

        self._db = db
        self._model = model

    #/**
    # * Set the database connection to be used
    # *
    # * @param Kohana_Database Database connection
    # * @return Minion_Migration_Manager
    # */
    def set_db(self, db):
        self._db = db

    #/**
    # * Set the model to be used in the rest of the app
    # *
    # * @param Model_Minion_Migration Model instance
    # * @return Minion_Migration_Manager
    # */
    def set_model(self, model):
        self._model = model

        return self

    #/**
    # * Set whether the manager should execute a dry run instead of a real run
    # *
    # * @param boolean Whether we should do a dry run
    # * @return Minion_Migration_Manager
    # */
    def set_dry_run(self, dry_run):
        self._dry_run = bool(dry_run)

        return self

    #/**
    # * Returns a set of queries that would've been executed had dry run not been
    # * enabled.  If dry run was not enabled, this returns an empty array
    # *
    # * @return array SQL Queries
    # */
    def get_dry_run_sql(self):
        return self._dry_run_sql

    #/**
    # * Returns a set of executed migrations
    # * @return array
    # */
    def get_executed_migrations(self):
        return self._executed_migrations

    #/**
    # * Run migrations in the specified groups so as to reach specified targets
    # *
    # *
    # *
    # * @param  array   Set of groups to update, empty array means all
    # * @param  array   Versions for specified groups
    # * @return array   Array of all migrations that were successfully applied
    # */
#	public function run_migration($group = array(), $target = TRUE)
#	{
#		list($migrations, $is_up) = $this->_model->fetch_required_migrations($group, $target);
#
#		$method = $is_up ? 'up' : 'down';
#
#		foreach ($migrations as $migration)
#		{
#			if ($method == 'down' AND $migration['timestamp'] <= Kohana::$config->load('minion/migration')->lowest_migration)
#			{
#				Minion_CLI::write(
#					'You\'ve reached the lowest migration allowed by your config: '.Kohana::$config->load('minion/migration')->lowest_migration,
#					'red'
#				);
#				return;
#			}
#
#			$filename  = $this->_model->get_filename_from_migration($migration);
#
#			if ( ! ($file  = Kohana::find_file('migrations', $filename, FALSE)))
#			{
#				throw new Kohana_Exception(
#					'Cannot load migration :migration (:file)',
#					array(
#						':migration' => $migration['id'],
#						':file'      => $filename
#					)
#				);
#			}
#
#			$class = $this->_model->get_class_from_migration($migration);
#
#			include_once $file;
#
#			$instance = new $class($migration);
#
#			$db = $this->_get_db_instance($instance->get_database_connection());
#
#			try
#			{
#				$instance->$method($db);
#			}
#			catch(Database_Exception $e)
#			{
#				throw new Minion_Migration_Exception($e->getMessage(), $migration);
#			}
#
#			if ($this->_dry_run)
#			{
#				$this->_dry_run_sql[$migration['group']][$migration['timestamp']] = $db->reset_query_stack();
#			}
#			else
#			{
#				$this->_model->mark_migration($migration, $is_up);
#			}
#
#			$this->_executed_migrations[] = $migration;
#		}
#	}

    #/**
    # * Syncs all available migration files with the database
    # *
    # * @chainable
    # * @return Minion_Migration_Manager Chainable instance
    # */
#	public function sync_migration_files()
#	{
#		// Get array of installed migrations with the id as key
#		$installed = $this->_model->fetch_all('id');
#
#		$available = $this->_model->available_migrations();
#
#		$all_migrations = array_merge(array_keys($installed), array_keys($available));
#
#		foreach ($all_migrations as $migration)
#		{
#			// If this migration has since been deleted
#			if (isset($installed[$migration]) AND ! isset($available[$migration]))
#			{
#				// We should only delete a record of this migration if it does
#				// not exist in the "real world"
#				if ($installed[$migration]['applied'] === '0')
#				{
#					$this->_model->delete_migration($installed[$migration]);
#				}
#			}
#			// If the migration has not yet been installed :D
#			elseif ( ! isset($installed[$migration]) AND isset($available[$migration]))
#			{
#				$this->_model->add_migration($available[$migration]);
#			}
#			// Somebody changed the description of the migration, make sure we
#			// update it in the db as we use this to build the filename!
#			elseif ($installed[$migration]['description'] !== $available[$migration]['description'])
#			{
#				$this->_model->update_migration($installed[$migration], $available[$migration]);
#			}
#		}
#
#		return $this;
#	}

    #/**
    # * Gets a database connection for running the migrations
    # *
    # * @param  string Database connection group name
    # * @return Kohana_Database Database connection
    # */
    def _get_db_instance(self, db_group):
        # if this isn't a dry run then just use a normal database connection
        if not self._dry_run:
            pass
#            return database:instance(db_group)# TODO

        return faux_instance(db_group)

#	protected function _get_db_instance($db_group)
#	{
#		// If this isn't a dry run then just use a normal database connection
#		if ( ! $this->_dry_run)
#			return Database::instance($db_group);
#
#		return Minion_Migration_Database::faux_instance($db_group);
#	}

