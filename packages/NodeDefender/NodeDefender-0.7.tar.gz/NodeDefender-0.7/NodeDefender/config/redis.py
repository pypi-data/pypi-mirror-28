import NodeDefender

config = {'enabled' : False}
default_config = {'enabled' : False,
                  'host' : '',
                  'port' : '',
                  'database' : ''}

def load_config(parser):
    config['enabled'] = eval(parser['REDIS']['ENABLED'])
    config['host'] = parser['REDIS']['HOST']
    config['port'] = parser['REDIS']['PORT']
    config['database'] = parser['REDIS']['DATABASE']
    NodeDefender.app.config.update(
        REDIS = config['enabled'],
        REDIS_HOST = config['host'],
        REDIS_PORT = config['port'],
        REDIS_DATABASE = config['database'])
    return True

def enabled():
    return config['enabled']

def host():
    return config['host']

def port():
    return config['port']

def database():
    return config['database']

def set_defaults():
    for key, value in default_config.items():
        NodeDefender.config.parser['REDIS'][key] = str(value)

def set_cfg(**kwargs):
    for key, value in kwargs.items():
        NodeDefender.config.parser['REDIS'][key] = str(value)

    return NodeDefender.config.write()
