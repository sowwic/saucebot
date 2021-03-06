import sys
import inspect
import pathlib
import logging
import logging.handlers


class Logger:

    LOGGER_NAME = 'saucebot'
    LEVEL_DEFAULT = logging.DEBUG
    PROPAGATE_DEFAULT = False
    FORMAT_DEFAULT = '[%(levelname)s] %(message)s'
    DATE_FORMAT = '%d-%m-%Y %H:%M:%S'
    _logger_obj: logging.Logger = None

    @classmethod
    def logger_obj(cls) -> logging.Logger:
        """Returns logger object

        :return: Logger object
        :rtype: logging.Logger
        """
        if not cls._logger_obj:
            if cls.logger_exists():
                cls._logger_obj = logging.getLogger(cls.LOGGER_NAME)
            else:
                cls._logger_obj = logging.getLogger(cls.LOGGER_NAME)
                cls._logger_obj.setLevel(cls.LEVEL_DEFAULT)
                cls.set_propagate(cls.PROPAGATE_DEFAULT)
                # Formatters
                fmt = logging.Formatter(cls.FORMAT_DEFAULT, datefmt=cls.DATE_FORMAT)
                # Handlers
                stream_handler = logging.StreamHandler(sys.stdout)
                stream_handler.setFormatter(fmt)
                cls._logger_obj.addHandler(stream_handler)

        return cls._logger_obj

    @classmethod
    def logger_exists(cls):
        return cls.LOGGER_NAME in logging.Logger.manager.loggerDict.keys()

    @classmethod
    def set_level(cls, level):
        lg = cls.logger_obj()
        lg.setLevel(level)

    @classmethod
    def get_level(cls, name=False):
        if name:
            return logging.getLevelName(cls.logger_obj().level)
        return cls.logger_obj().level

    @classmethod
    def set_propagate(cls, propagate):
        lg = cls.logger_obj()
        lg.propagate = propagate

    @classmethod
    def signal_handler(cls):
        cls.logger_obj()
        return cls._signal_handler

    @classmethod
    def call_info(cls, message: str):
        caller = inspect.getframeinfo(inspect.stack()[1][0])
        message = 'file: {0} function {1}() lineno:{2}-{3}'.format(caller.filename, caller.function, caller.lineno, message)

    @classmethod
    def debug(cls, msg: str, *args, **kwargs):
        lg = cls.logger_obj()
        lg.debug(msg, *args, **kwargs)

    @classmethod
    def info(cls, msg: str, *args, **kwargs):
        lg = cls.logger_obj()
        lg.info(msg, *args, **kwargs)

    @classmethod
    def warning(cls, msg: str, *args, **kwargs):
        lg = cls.logger_obj()
        lg.warning(msg, *args, **kwargs)

    @classmethod
    def error(cls, msg: str, *args, **kwargs):
        lg = cls.logger_obj()
        lg.error(msg, *args, **kwargs)

    @classmethod
    def critical(cls, msg: str, *args, **kwargs):
        lg = cls.logger_obj()
        lg.critical(msg, *args, **kwargs)

    @classmethod
    def log(cls, level, msg: str, *args, **kwargs):
        lg = cls.logger_obj()
        lg.log(level, msg, *args, **kwargs)

    @classmethod
    def exception(cls, msg: str, *args, **kwargs):
        lg = cls.logger_obj()
        lg.exception(msg, *args, **kwargs)

    @classmethod
    def write_to_rotating_file(cls, path: str, level=logging.ERROR, mode: str = 'w', max_bytes: int = 512):
        if isinstance(path, pathlib.Path):
            path = path.as_posix()

        lg = cls.logger_obj()
        if any([isinstance(handler, logging.handlers.RotatingFileHandler) for handler in lg.handlers]):
            lg.warning('Rotating file hander already exists')
            return

        rfile_hander = logging.handlers.RotatingFileHandler(path, mode=mode, maxBytes=max_bytes, backupCount=0, delay=0)
        rfile_hander.setLevel(level)
        fmt = logging.Formatter('[%(asctime)s][%(levelname)s] %(message)s')
        rfile_hander.setFormatter(fmt)
        lg.addHandler(rfile_hander)
        cls.info('Logging to file {}'.format(path))
