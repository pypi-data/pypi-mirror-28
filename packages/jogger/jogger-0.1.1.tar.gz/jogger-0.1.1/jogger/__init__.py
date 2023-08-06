import logging, textwrap,  yaml, os

message = textwrap.dedent('''\
    No logger available.
    Init a logger by calling the function 'init_logger'.''')

config_file = '~/.jogger.yml'

class Logger():
    logger = None

    @classmethod
    def create(cls, logger_name):
        if not Logger.logger:
            Logger.logger = logging.getLogger(logger_name)
            Logger.logger.setLevel(logging.INFO)

            file_path = os.path.expanduser(config_file)
            if os.path.isfile(file_path):
                with open(file_path, 'r') as stream:
                    handlers = yaml.safe_load(stream.read())
                    if handlers:
                        for key in handlers:
                            code = handlers[key]
                            handler = _load_handler(key, code)
                            Logger.logger.addHandler(handler)


def _load_handler(key, code):
    data = {}
    exec(code, data)
    if 'handler' in  data:
        return data['handler']
    else:
        raise Exception('No handler found in {}'.format(key))


def init_logger(logger_name):
    Logger.create(logger_name)


def debug(*args, **kwargs):
    if Logger.logger:
        Logger.logger.debug(*args, **kwargs)
    else:
        raise Exception(message)


def info(*args, **kwargs):
    if Logger.logger:
        Logger.logger.info(*args, **kwargs)
    else:
        raise Exception(message)


def warning(*args, **kwargs):
    if Logger.logger:
        Logger.logger.warning(*args, **kwargs)
    else:
        raise Exception(message)


def error(*args, **kwargs):
    if Logger.logger:
        Logger.logger.error(*args, **kwargs)
    else:
        raise Exception(message)


def critical(*args, **kwargs):
    if Logger.logger:
        Logger.logger.critical(*args, **kwargs)
    else:
        raise Exception(message)
