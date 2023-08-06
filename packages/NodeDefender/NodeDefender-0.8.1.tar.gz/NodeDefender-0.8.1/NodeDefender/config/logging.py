import NodeDefender

default_config = {'enabled' : False,
                  'level' : 'DEBUG',
                  'type' : '',
                  'filepath' : '',
                  'host' : '',
                  'port' : ''}

config = default_config.copy()

def load_config(parser):
    config['enabled'] = eval(parser['LOGGING']['ENABLED'])
    config['level'] = parser['LOGGING']['LEVEL']
    config['type'] = parser['LOGGING']['TYPE']
    config['filepath'] = parser['LOGGING']['FILEPATH']
    config['host'] = parser['LOGGING']['HOST']
    config['port'] = parser['LOGGING']['PORT']
    NodeDefender.app.config.update(
        LOGGING = config['enabled'],
        LOGGING_LEVEL = config['level'],
        LOGGING_TYPE = config['type'],
        LOGGING_FILEPATH = config['filepath'],
        LOGGING_HOST = config['host'],
        LOGGING_PORT = config['port'])
    return True

def enabled():
    return config['enabled']

def level():
    return config['level']

def type():
    return config['type']

def filepath():
    return config['filepath']

def host():
    return config['host']

def port():
    return config['port']

def set_defaults():
    for key, value in default_config.items():
        NodeDefender.config.parser['LOGGING'][key] = str(value)
    return True

def set_cfg(**kwargs):
    for key, value in kwargs.items():
        NodeDefender.config.parser['LOGGING'][key] = str(value)

    return NodeDefender.config.write()
