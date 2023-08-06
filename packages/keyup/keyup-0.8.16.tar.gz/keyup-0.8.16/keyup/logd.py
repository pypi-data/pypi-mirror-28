"""
Project-level logging module

"""
import inspect
import logging
import logging.handlers

from keyup.statics import local_config

syslog = logging.getLogger()
syslog.setLevel(logging.DEBUG)


def mode_assignment(arg):
    """
    Translates arg to enforce proper assignment
    """
    arg = arg.upper()
    stream_args = ('STREAM', 'CONSOLE', 'STDOUT')
    try:
        if arg in stream_args:
            return 'STREAM'
        else:
            return arg
    except Exception:
        return None


def getLogger(*args, **kwargs):
    """
    Summary:
        custom format logger

    Args:
        mode (str):  The Logger module supprts the following log modes:

            - log to console / stdout. Log_mode = 'stream'
            - log to file
            - log to system logger (syslog)

    Returns:
        logger object | TYPE: logging
    """
    # args
    log_mode = local_config['LOGGING']['LOG_MODE']
    logger = logging.getLogger(*args, **kwargs)
    logger.propagate = False

    try:
        if not logger.handlers:
            # branch on output format, default to stream
            if mode_assignment(log_mode) == 'FILE':
                # file handler
                f_handler = logging.FileHandler(local_config['LOGGING']['LOG_PATH'])
                f_formatter = logging.Formatter('%(asctime)s - %(pathname)s - %(name)s - [%(levelname)s]: %(message)s')
                # f_formatter = logging.Formatter('%(asctime)s %(processName)-10s %(name)s [%(levelname)-5s]: %(message)s')
                f_handler.setFormatter(f_formatter)
                logger.addHandler(f_handler)
                logger.setLevel(logging.DEBUG)

            elif mode_assignment(log_mode) == 'STREAM':
                # stream handlers
                s_handler = logging.StreamHandler()
                s_formatter = logging.Formatter('%(pathname)s - %(name)s - [%(levelname)s]: %(message)s')
                s_handler.setFormatter(s_formatter)
                logger.addHandler(s_handler)
                logger.setLevel(logging.DEBUG)

            elif mode_assignment(log_mode) == 'SYSLOG':
                sys_handler = logging.handlers.SysLogHandler(address = '/dev/log')
                sys_formatter = logging.Formatter('%(asctime)s - %(pathname)s - %(name)s - [%(levelname)s]: %(message)s')
                sys_handler.setFormatter(sys_formatter)
                logger.addHandler(sys_handler)
                logger.setLevel(logging.DEBUG)

            else:
                syslog.warning(
                    '%s: [WARNING]: log_mode value of (%s) unrecognized - not supported' %
                    (inspect.stack()[0][3], str(log_mode))
                    )
                ex = Exception(
                    '%s: Unsupported mode indicated by log_mode value: %s' %
                    (inspect.stack()[0][3], str(log_mode))
                    )
                raise ex
    except OSError as e:
        raise e
    return logger
