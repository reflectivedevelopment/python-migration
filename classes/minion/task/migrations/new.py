from classes.minion.task import minion_task
from classes.model.minion.migration import MIGRATION_DIR
import datetime
import os
import re

#/**
# * The new task provides an easy way to create migration files
# *
# * Available config options are:
# *
# * --group=group_name
# *
# *  This is a required config option, use it specify in which group the
# *  migration should be stored. Migrations are stored in a `migrations`
# *  directory followed by the group name specified. By default, the `migrations`
# *  directory is created in `APPPATH` but that can be changed with `--location`
# *
# * --location=modules/auth
# *
# *  Specified the path of the migration (without the `migrations` directory).
# *  This value is defaulted to `APPPATH`
# *
# *  # The migration will be created in `modules/myapp/migrations/myapp/`
# *  --group=myapp --location=modules/myapp
# *
# * --description="Description of migration here"
# *
# *  This is an arbitrary description of the migration, used to build the
# *  filename.  It is required but can be changed manually later on without
# *  affecting the integrity of the migration.
# *
# */
class minion_task_migrations_new(minion_task):
#	/**
#	 * A set of config options that this task accepts
#	 * @var array
#	 */
    _config = [
        'group',
        'description',
        'location'
        ]

#	/**
#	 * Execute the task
#	 *
#	 * @param array Configuration
#	 */
    def execute(self, config):
        try:
            file = self.generate(config)
            print 'Migration generated: %s' % file
        except Exception as e:
            raise e
#		}
#		catch(ErrorException $e)
#		{
#			Minion_CLI::write($e->getMessage());
#		}
#
#	}
#
    def generate(self, config, up=None, down=None):
        defaults = {
#			'location'    => APPPATH,
            'description': '',
            'group': ''
        }

        config = dict(defaults.items() + config.items())

#		// Trim slashes in group
        config['group'] = config['group'].strip('/')

        print config

        if not self._valid_group(config['group']):
            raise Exception('Please provide a valid --group')

        group = '%s/' % config['group']
        description = config['description']
        location = MIGRATION_DIR

#		// {year}{month}{day}{hour}{minute}{second}
        
        time = datetime.datetime.now().strftime("%Y%m%d%H%M%S")
        classname = self._generate_classname(group, time)
        file = self._generate_filename(location, group, time, description)

        data = '''from classes.minion.migration.base import minion_migration_base

class migration(minion_migration_base):
    description = '%s'

    def up(self, db):
        pass

    def down(self, db):
        pass''' % description

        if not os.path.exists(os.path.dirname(file)):
            os.makedirs(os.path.dirname(file), 0775)

        outfile = open(file, 'w')

        outfile.write(data)

        outfile.close()

        return file

#	/**
#	 * Generate a class name from the group
#	 *
#	 * @param  string group
#	 * @param  string Timestamp
#	 * @return string Class name
#	 */
    def _generate_classname(self, group, time):
        return 'migration'
#		$class = ucwords(str_replace('/', ' ', $group));
#
#		// If group is empty then we want to avoid double underscore in the
#		// class name
#		if ( ! empty($class))
#		{
#			$class .= '_';
#		}
#
#		$class .= $time;
#
#		return 'Migration_'.preg_replace('~[^a-zA-Z0-9]+~', '_', $class);
#	}
#
#	/**
#	 * Generates a filename from the group, time and description
#	 *
#	 * @param  string Location to store migration
#	 * @param  string Timestamp
#	 * @param  string Description
#	 * @return string Filename
#	 */
    def _generate_filename(self, location, group, time, description):
        
#		// Max 100 characters, lowecase filenames.
        label = description[0:100]
#		// Only letters
        label = re.sub('[^A-Za-z]+', '-', label)
#		// Add the location, group, and time
        filename = os.path.join(location, group, '%s_%s' % (time, label))
#		// If description was empty, trim underscores
        filename = filename.strip('_')
        filename = '%s.py' % filename

        return filename

    def _valid_group(self, group):
#		// Group cannot be empty
        if len(group) <= 0:
            return False

#		// Can only consist of alpha-numeric values, dashes, underscores, and slashes
        if re.search('[^a-zA-Z0-9\/_-]', group):
            return False

#		// Must also contain at least one alpha-numeric value
        if not re.search('[a-zA-Z0-9]', group):
            return False # return FALSE; // --group="/" breaks things but "a/b" should be allowed

        return True
