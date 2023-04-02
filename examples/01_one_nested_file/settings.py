import gemtoolsconfig

config = gemtoolsconfig.quick_setup('conf')

APP_NAME = config['app']['name']
APP_VERSION = config['app']['version']

DEBUG_ENABLED = config['debug']['enabled']
DEBUG_LEVEL = config['debug']['level']
