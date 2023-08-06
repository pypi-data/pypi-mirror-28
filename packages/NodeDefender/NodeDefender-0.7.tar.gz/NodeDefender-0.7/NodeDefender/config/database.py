import NodeDefender

config = {'enabled' : False}
default_config = {'enabled' : False,
                  'engine' : '',
                  'username' : '',
                  'password' : '',
                  'host' : '',
                  'port' : '',
                  'database' : '',
                  'filepath' : ''}

def load_config(parser):
    config['enabled'] = eval(parser['DATABASE']['ENABLED'])
    config['engine'] = parser['DATABASE']['ENGINE']
    config['username'] = parser['DATABASE']['USERNAME']
    config['password'] = parser['DATABASE']['PASSWORD']
    config['host'] = parser['DATABASE']['HOST']
    config['port'] = parser['DATABASE']['PORT']
    config['database'] = parser['DATABASE']['DATABASE']
    config['filepath'] = parser['DATABASE']['FILEPATH']
    NodeDefender.app.config.update(
        DATABASE = config['enabled'],
        DATABASE_ENGINE = config['engine'],
        DATABASE_USERNAME = config['username'],
        DATABASE_PASSWORD = config['password'],
        DATABASE_HOST = config['host'],
        DATABASE_PORT = config['port'],
        DATABASE_DATABASE = config['database'],
        DATABASE_FILEPATH = config['filepath'])
    if NodeDefender.app.testing:
        NodeDefender.app.config.update(
            SQLALCHEMY_DATABASE_URI = "sqlite:///:memory:")
    else:
        NodeDefender.app.config.update(
            SQLALCHEMY_DATABASE_URI = get_uri())
    return config

def get_uri():
    db_engine = engine()
    if config['engine'] == 'sqlite':
        return 'sqlite:///' + NodeDefender.config.parser['DATABASE']['FILEPATH']
    
    username = config['username']
    password = config['password']
    host = config['host']
    port = config['port']
    database = config['database']
    if config['engine'] == 'mysql':
        return 'mysql+pymysql://'+username+':'+password+'@'+host+':'+port+\
            '/'+database
    elif config['engine'] == 'postgresql':
        return 'postgresql://'+username+':'+password+'@'+host+':'+port+\
                '/'+database()
    return "sqlite:///:memory:"

def enabled():
    return config['enabled']

def engine():
    return config['engine']

def username():
    return config['username']

def password():
    return config['password']

def host():
    return config['host']

def port():
    return config['port']

def database():
    return config['database']

def filepath():
    return config['filepath']

def mysql_uri():
    return 'mysql+pymysql://'+username()+':'+password()+'@'+host()+':'+port()\
            +'/'+database()

def postgresql_uri():
    return 'postgresql://'+username()+':'+password()+'@'\
            +host()+':'+port()+'/'+database()

def sqlite_uri():
    return 'sqlite:///' + filepath()

def uri():
    db_engine = engine()
    return eval(db_engine + '_uri')()

def set_defaults():
    for key, value in default_config.items():
        NodeDefender.config.parser['DATABASE'][key] = str(value)
    return True

def set_config(**kwargs):
    for key, value in kwargs.items():
        NodeDefender.config.parser['DATABASE'][key] = str(value)

    return NodeDefender.config.write()
