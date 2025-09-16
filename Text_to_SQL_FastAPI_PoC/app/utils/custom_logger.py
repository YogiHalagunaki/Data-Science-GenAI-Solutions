import os
import logging
import traceback
from functools import partial

class CustomFormatter(logging.Formatter):
    """
    This CustomFormatter can be used to have custom formats and custom color codings based on 
    differnt logging levels.

    For ANSI color coding, refer this-
    https://gist.github.com/raghav4/48716264a0f426cf95e4342c21ada8e7
    """
    def __init__(self, module):
        self.module = module

    # color codes
    reset = "\x1b[0m"
    white = "\x1b[37m"                      # for info messages
    grey = "\x1b[38;20m"
    yellow = "\x1b[33;20m"                  # for warnings
    bold_red = "\x1b[31;1m"                 # for errors
    bold_underline_red = "\x1b[31;1;4m"     # for critical messages
    light_green = "\x1b[92m"                # for debug messages 

    # format = "%(asctime)s - %(name)s - %(levelname)s - %(message)s (%(filename)s:%(lineno)d)"
    format_general = '-%(asctime)s, %(module)s, %(levelname)s, %(filename)s, %(lineno)d, "message": "%(message)s"'
    format_info = '-(%(levelname)s: %(module)s): %(message)s'
    format_debug = '* * * * * * * * * * DEBUG * * * * * * * * * *\n%(message)s'
    format_error = '-(%(levelname)s: %(module)s: %(filename)s: at line %(lineno)d): %(message)s'
    # format_error = '(%(levelname)s:: %(filename)s:: %(lineno)d): %(message)s: %(exc_text)s'

    FORMATS = {
        # logging.DEBUG: light_green + format_debug + reset,
        # logging.INFO: white + format_info + reset,
        # logging.WARNING: yellow + format + reset,
        # logging.ERROR: bold_red + format_error + reset,
        # logging.CRITICAL: bold_underline_red + format + reset
        logging.DEBUG: format_debug,
        logging.INFO: format_general,
        logging.WARNING: format_general,
        logging.ERROR: format_general,
        logging.CRITICAL: format_general
    }

    def format(self, record):
        record.module = self.module
        
        # remove all newline characters and replace them by ';'
        if isinstance(record.msg, str):
            record.msg = record.msg.replace('\n', ' ; ')
        
        # exc_text attribute to add traceback of the record(used for error)
        if record.exc_info:
            exc_text = ''.join(traceback.format_exception(*record.exc_info))
            record.exc_text = exc_text
        else:
            record.exc_text = ''
        
        log_fmt = self.FORMATS.get(record.levelno)
        formatter = logging.Formatter(log_fmt, datefmt= '%Y-%m-%d %H:%M:%S')
        return formatter.format(record)
    
def get_logger(module: str, file_handler=False):    
    
    # creating new logger object
    logger = logging.getLogger()                            

    # log mode set as INFO
    logger.setLevel(os.getenv("log_level", "INFO"))  

    # get traceback stack of the all error are listed
    logger.error = partial(logger.error, exc_info=True)     
    
    # creating handler for showing the logs on console
    handler_console = logging.StreamHandler()         
    
    # set CustomFormatter to the handler
    handler_console.setFormatter(CustomFormatter(module=module))    
    
    logger.addHandler(handler_console)

    if file_handler:

        # handler for writing logs in file
        handler_file = logging.FileHandler('log_file.log')   
            
        # set CustomFormatter to the handler       
        handler_file.setFormatter(CustomFormatter(module=module))       
        logger.addHandler(handler_file)
    
    return logger
