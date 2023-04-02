from gemtoolsconfig import Configurations, preset_file_loader

Configurations.add_loader(preset_file_loader('conf', key_file='config.key'))
config = Configurations.get_config()

APP_NAME = config['app']['name']
APP_VERSION = config['app']['version']

DEBUG_ENABLED = config['debug']['enabled']
DEBUG_LEVEL = config['debug']['level']
