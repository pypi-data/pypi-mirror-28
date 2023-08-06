from datetime import datetime
import NodeDefender

config = {'run_mode' : 'TESTING',
          'key' : 'key',
          'salt' : 'salt',
          'host' : '0.0.0.0',
          'port' : '50000',
          'self_registration' : True}

default_config = {'run_mode' : 'TESTING',
                  'key' : 'key',
                  'salt' : 'salt',
                  'host' : '0.0.0.0',
                  'port' : '50000',
                  'self_registration' : True}

def load_config(parser):
    config['run_mode'] = parser['GENERAL']['RUN_MODE']
    config['key'] = parser['GENERAL']['KEY']
    config['salt'] = parser['GENERAL']['SALT']
    config['host'] = parser['GENERAL']['host']
    config['port'] = int(parser['GENERAL']['port'])
    config['self_registration'] = eval(parser['GENERAL']['SELF_REGISTRATION'])
    NodeDefender.app.config.update(
        RUN_MODE = config['run_mode'],
        SECRET_KEY = config['key'],
        SECRET_SALT = config['salt'],
        SERVER_NAME = config['host'])

    if config['run_mode'].upper() == 'DEVELOPMENT':
        NodeDefender.app.config.update(DEBUG = True)
    elif config['run_mode'].upper() == 'TESTING':
        NodeDefender.app.config.update(
            DEBUG = True,
            TESTING = True)
    return True

def hostname():
    return os.uname().nodename

def uptime():
    return str(datetime.now() - _loaded_at)

def run_mode():
    return config['run_mode']

def key():
    return config['key']

def salt():
    return config['salt']

def host():
    return config['host']

def server_port():
    return config['port']

def self_registration():
    return config['self_registration']

def set_defaults():
    for key, value in default_config.items():
        NodeDefender.config.parser['GENERAL'][key] = str(value)
    return True

def set_cfg(**kwargs):
    for key, value in kwargs.items():
        NodeDefender.config.parser['GENERAL'][key] = str(value)

    return NodeDefender.config.write()
