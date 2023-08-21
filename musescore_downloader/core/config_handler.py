import os
import logging
import configparser

def initialize_config_handler(filename=None):
    cfg_parser = configparser.ConfigParser(interpolation=None)
    
    if filename is not None:
        cfg_parser.read_file(open(filename))
    elif os.path.isfile(os.path.join(os.getcwd(), "config.ini")):
        cfg_parser.read_file(open("config.ini"))
    else:
        logging.warning("The config parser has not been initialized with a file.")
    
    return cfg_parser
