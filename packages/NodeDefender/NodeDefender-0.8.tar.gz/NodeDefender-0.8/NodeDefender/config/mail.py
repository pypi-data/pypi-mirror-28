import NodeDefender

config = {'enabled' : False}
default_config = {'enabled' : False,
                  'host' : '',
                  'port' : 465,
                  'tls' : False,
                  'ssl' : False,
                  'username' : '',
                  'password' : ''}

def load_config(parser):
    config['enabled'] = eval(parser['MAIL']['ENABLED'])
    config['host'] = parser['MAIL']['HOST']
    config['port'] = parser['MAIL']['PORT']
    config['tls'] = eval(parser['MAIL']['TLS'])
    config['ssl'] = eval(parser['MAIL']['SSL'])
    config['username'] = parser['MAIL']['USERNAME']
    config['password'] = parser['MAIL']['PASSWORD']
    NodeDefender.app.config.update(
        MAIL = config['enabled'],
        MAIL_HOST = config['host'],
        MAIL_PORT = config['port'],
        MAIL_TLS = config['tls'],
        MAIL_SSL = config['ssl'],
        MAIL_USERNAME = config['username'],
        MAIL_PASSWORD = config['password'])
    return True

def enabled():
    return config['enabled']

def host():
    return config['host']

def port():
    return config['port']

def tls():
    return config['tls']

def ssl():
    return config['ssl']

def username():
    return config['username']

def password():
    return config['password']

def set_defaults():
    for key, value in default_config.items():
        NodeDefender.config.parser['MAIL'][key] = str(value)
    return True

def set_cfg(**kwargs):
    for key, value in kwargs.items():
        NodeDefender.config.parser['MAIL'][key] = str(value)

    return NodeDefender.config.write()
