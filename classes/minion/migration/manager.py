from classes.model.minion.migration import model_minion_migration as migration_model
from classes.minion.migration.database import faux_instance
from classes.minion.database.base import instance as database

#/**
# * The migration manager is responsible for locating migration files, syncing
# * them with the migrations table in the database and selecting any migrations
# * that need to be executed in order to reach a target version
# *
# * @author Matt Button <matthew@sigswitch.com>
# */

class minion_migration_manager():
    #/**
    # * Constructs the object, allows injection of a Database connection
    # *
    # * @param Kohana_Database        The database connection that should be passed to migrations
    # * @param Model_Minion_Migration Inject an instance of the minion model into the manager
    # */
    def __init__(self, db, model=None):

        #/**
        # * The database connection that sould be used
        # * @var Kohana_Database
        # */
        self._db = None

        #/**
        # * Model used to interact with the migrations table in the database
        # * @var Model_Minion_Migration
        # */
        self._model = None

        #/**
        # * Whether this is a dry run migration
        # * @var boolean
        # */
        self._dry_run = False

        #/**
        # * A set of SQL queries that were generated on the dry run
        # * @var array
        # */
        self._dry_run_sql = {}

        #/**
        # * Set of migrations that were executed
        # */
        self._executed_migrations = []

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
    def run_migrations(self, group={}, target=True):
        (migrations, is_up) = self._model.fetch_required_migrations(group, target)

        method = 'up' if is_up else 'down'

        for migration in migrations:
            # Config allows limiting how low you go. TODO
#            if method == 'down' and migration['timestamp'] <= 
#			if ($method == 'down' AND $migration['timestamp'] <= Kohana::$config->load('minion/migration')->lowest_migration)
#			{
#				Minion_CLI::write(
#					'You\'ve reached the lowest migration allowed by your config: '.Kohana::$config->load('minion/migration')->lowest_migration,
#					'red'
#				);
#				return;
#			}

            filename = self._model.get_filename_from_migration(migration)

            include_name = self._model.get_class_from_migration(migration)

            instance = __import__(include_name, fromlist=[include_name])

            instance_migration = instance.migration(migration)

            db = self._get_db_instance(instance_migration.get_database_connection())

            try:
                instance_func = getattr(instance_migration, method)

                instance_func(db)
            except Exception as e:
                raise e
#				throw new Minion_Migration_Exception($e->getMessage(), $migration);

            if self._dry_run:
                self._dry_run_sql[migration['group']][migration['timestamp']] = db.reset_query_stack()
            else:
                self._model.mark_migration(migration, is_up)

            self._executed_migrations.append(migration)

    #/**
    # * Syncs all available migration files with the database
    # *
    # * @chainable
    # * @return Minion_Migration_Manager Chainable instance
    # */
    def sync_migration_files(self):
#		// Get array of installed migrations with the id as key
        installed = self._model.fetch_all('id')

        available = self._model.available_migrations()

        all_migrations = installed.keys() + available.keys()

        for migration in all_migrations:
#			// If this migration has since been deleted
            if installed.has_key(migration) and (not available.has_key(migration)):
#				// We should only delete a record of this migration if it does
#				// not exist in the "real world"
                if installed[migration]['applied'] == 0:
                    self._model.delete_migration(installed[migration])
#			// If the migration has not yet been installed :D
            elif (not installed.has_key(migration)) and available.has_key(migration):
                self._model.add_migration(available[migration])
#			// Somebody changed the description of the migration, make sure we
#			// update it in the db as we use this to build the filename!
            elif installed[migration]['description'] != available[migration]['description']:
                self._model.update_migration(installed[migration], available[migration])

        return self
    
    #/**
    # * Gets a database connection for running the migrations
    # *
    # * @param  string Database connection group name
    # * @return Kohana_Database Database connection
    # */
    def _get_db_instance(self, db_group):
        # if this isn't a dry run then just use a normal database connection
        if not self._dry_run:
            return database(db_group)

        return faux_instance(db_group)

