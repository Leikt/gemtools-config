from gemtoolsconfig import Configurations, preset_file_loader

Configurations.add_loader(preset_file_loader('conf'))
config_app = Configurations.get_config('app')
config_debug = Configurations.get_config('debug')

APP_NAME = config_app['name']
APP_VERSION = config_app['version']

DEBUG_ENABLED = config_debug['enabled']
DEBUG_LEVEL = config_debug['level']
