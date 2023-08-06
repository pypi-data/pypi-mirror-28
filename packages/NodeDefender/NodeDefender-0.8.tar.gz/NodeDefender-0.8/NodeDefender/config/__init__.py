import NodeDefender
import NodeDefender.config.celery 
import NodeDefender.config.database
import NodeDefender.config.general
import NodeDefender.config.logging
import NodeDefender.config.mail
import NodeDefender.config.redis
import configparser
import os

filename = None

parser = configparser.ConfigParser()
basepath = os.path.abspath(os.path.dirname('..'))

def find_configfile():
    if os.path.exists("NodeDefender.conf"):
        return "NodeDefender.conf"
    
    home_dir = os.path.expanduser('~')
    if os.path.exists(home_dir + '.config/nodedefender/NodeDefender.conf'):
        return home_dir + '.config/nodedefender/NodeDefender.conf'
    else:
        raise NotImplementedError("Config- file not found")

def write_default():
    NodeDefender.config.celery.set_defaults()
    NodeDefender.config.database.set_defaults()
    NodeDefender.config.general.set_defaults()
    NodeDefender.config.logging.set_defaults()
    NodeDefender.config.mail.set_defaults()
    NodeDefender.config.redis.set_defaults()
    return write()

def load(fname = None):
    global filename
    if fname is None:
        fname = find_configfile()

    if not os.path.exists(fname):
        raise ValueError("File not does exists")
    
    if not os.access(fname, os.R_OK):
        raise AttributeError("Read and/or write permission not set")

    filename = fname
    parser.read(filename)
    NodeDefender.config.celery.load_config(parser)
    NodeDefender.config.database.load_config(parser)
    NodeDefender.config.general.load_config(parser)
    NodeDefender.config.logging.load_config(parser)
    NodeDefender.config.mail.load_config(parser)
    NodeDefender.config.redis.load_config(parser)
    return True

def write():
    with open(filename, 'w') as fw:
        parser.write(fw)
