from classes.minion.task import minion_task
from config import migration as migration_conf
from classes.minion.database import base as database
from classes.model.minion.migration import model_minion_migration as migration_model
from classes.minion.migration.manager import minion_migration_manager as minion_migration_manager

#/**
# * The Run task compares the current version of the database with the target
# * version and then executes the necessary commands to bring the database up to
# * date
# *
# * Available config options are:
# *
# * --down
# *
# *   Migrate the group(s) down
# *
# * --up
# *
# *   Migrate the group(s) up
# *
# * --to=(timestamp|+up_migrations|down_migrations)
# *
# *   Migrate to a specific timestamp, or up $up_migrations, or down $down_migrations
# *
# *   Cannot be used with --groups, must be used with --group
# *
# * --group=group
# *
# *   Specify a single group to perform migrations on
# *
# * --groups=group[,group2[,group3...]]
# *
# *   A list of groups that will be used to source migration files.  By default
# *   migrations will be loaded from all available groups.
# *
# *   Note, only --up and --down can be used with --groups
# *
# * --dry-run
# *
# *  No value taken, if this is specified then instead of executing the SQL it
# *  will be printed to the console
# *
# * --quiet
# *
# *  Suppress all unnecessary output.  If --dry-run is enabled then only dry run
# *  SQL will be output
# *
# */

class minion_task_migrations_run(minion_task):
#	/**
#	 * A set of config options that this task accepts
#	 * @var array
#	 */
    _config = [
        'group',
        'groups',
        'up',
        'down',
        'to',
        'dry-run',
        'quiet'
        ]

#	/**
#	 * Migrates the database to the version specified
#	 *
#	 * @param array Configuration to use
#	 */
    def execute(self, config):
        k_config = migration_conf.conf()

        groups = config.get('group')
        target = config.get('to')

        dry_run = False
        quiet = False
        up = False
        down = False

        if config.get('dry-run'):
            dry_run = True
        if config.get('quiet'):
            quiet = True
        if config.get('up'):
            up = True
        if config.get('down'):
            down = True

        groups = self._parse_groups(groups)

        if target is None:
           if down:
               target = False
           else:
               target = True

        db = database.instance()
	model = migration_model(db)

        model.ensure_table_exists()

        manager = minion_migration_manager(db, model)

        # Sync the available migrations with those in the db
        manager.sync_migration_files().set_dry_run(dry_run)
#
#		$manager = new Minion_Migration_Manager($db, $model);
#
#		$manager
#			// Sync the available migrations with those in the db
#			->sync_migration_files()
#			->set_dry_run($dry_run);

#		try
#		{
#			// Run migrations for specified groups & versions
#			$manager->run_migration($groups, $target);
#		}
#		catch(Minion_Migration_Exception $e)
#		{
#			echo View::factory('minion/task/migrations/run/exception')
#				->set('migration', $e->get_migration())
#				->set('error',     $e->getMessage());
#
#			throw $e;
#		}

#		$view = View::factory('minion/task/migrations/run')
#			->set('dry_run', $dry_run)
#			->set('quiet', $quiet)
#			->set('dry_run_sql', $manager->get_dry_run_sql())
#			->set('executed_migrations', $manager->get_executed_migrations())
#			->set('group_versions', $model->get_group_statuses());
#
#		return $view;
#	}

#	/**
#	 * Parses a comma delimited set of groups and returns an array of them
#	 *
#	 * @param  string Comma delimited string of groups
#	 * @return array  Locations
#	 */
    def _parse_groups(self, group):
        if group is None:
            return []

        if isinstance(group, (list, tuple)):
            return group

        group = group.strip()

        if len(group) == 0:
            return []

        groups = []

        group = group.strip(',').split(',')

        if len(group) > 0:
            for a_group in group:
                groups.append(a_group.strip('/'))

        return groups

#	/**
#	 * Parses a set of target versions from user input
#	 *
#	 * Valid input formats for targets are:
#	 *
#	 *    TRUE
#	 *
#	 *    FALSE
#	 *
#	 *    {group}:(TRUE|FALSE|{migration_id})
#	 *
#	 * @param  string Target version(s) specified by user
#	 * @return array  Versions
#	 */
#	protected function _parse_target_versions($versions)
#	{
#		if (empty($versions))
#			return array();

#		$targets = array();

#		if ( ! is_array($versions))
#		{
#			$versions = explode(',', trim($versions));
#		}

#		foreach ($versions as $version)
#		{
#			$target = $this->_parse_version($version);

#			if (is_array($target))
#			{
#				list($group, $version) = $target;

#				$targets[$group] = $version;
#			}
#			else
#			{
#				$this->_default_direction = $target;
#			}
#		}

#		return $targets;
#	}

#	/*
#	 * Helper function for parsing target versions in user input
#	 *
#	 * @param  string         Input migration target
#	 * @return boolean|string The parsed target
#	 */
#	protected function _parse_version($version)
#	{
#		if (is_bool($version))
#			return $version;

#		if ($version === 'TRUE' OR $version == 'FALSE')
#			return $version === 'TRUE';

#		if (strpos($version, ':') !== FALSE)
#			return explode(':', $version);

#		throw new Kohana_Exception('Invalid target version :version', array(':version' => $version));
#	}

