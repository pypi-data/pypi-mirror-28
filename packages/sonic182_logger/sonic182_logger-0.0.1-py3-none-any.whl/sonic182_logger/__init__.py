"""Custom logger module."""
import logging
import collections
from uuid import uuid4

FMT = logging.Formatter(
    '{asctime}; LEVEL={levelname}; uuid={uuid}; type={type}; {message}',
    style='{'
)


class SonicAdapter(logging.LoggerAdapter):
    """Handle extra params for logging message."""

    def __init__(self, logger, extra=None, **kwargs):
        """Init log adapter."""
        self.ignore = kwargs.pop('ignore', [])
        self.hidden = kwargs.pop('hidden', [])
        super(SonicAdapter, self).__init__(logger, extra)

    def process(self, msg, kwargs):
        """Proccess message."""
        data, kwargs = self.setup_kwargs_data(msg, kwargs)
        return self._parse_data(data), kwargs

    def setup_kwargs_data(self, msg, kwargs=None):
        """Configure data to be logged."""
        data = kwargs.pop('data', {})
        extra = self.extra or {}
        extra = {**extra, **kwargs.pop('extra', {})}
        extra['uuid'] = extra.get('uuid', uuid4().hex)
        extra['type'] = msg
        kwargs['extra'] = extra
        return collections.OrderedDict(sorted(data.items())), kwargs

    def _parse_data(self, extra, key=''):
        """Append data params recursively.

        TODO: change to secuential implementation.
        """
        res = ''
        if isinstance(extra, dict):
            for _key, value in collections.OrderedDict(extra).items():
                temp_key = '{}{}{}'.format(key, ('.' if key else ''), _key)
                res += self._parse_data(value, temp_key)
        elif isinstance(extra, list):
            for ind, item in enumerate(extra):
                temp_key = '{}{}{}'.format(key, ('.' if key else ''), ind)
                res += self._parse_data(item, temp_key)
        else:
            return res + self.log_data(key, extra)
        return res

    def log_data(self, key, value):
        """Log data folowwing some rules."""
        if key in self.ignore:
            return ''
        elif key in self.hidden:
            return '{}={}'.format(key, ''.rjust(len(value), '*'))
        return '{}={}; '.format(key, value)


class LevelFilter(logging.Filter):
    """Custom logger filter."""

    def __init__(self, name='', **kwargs):
        """Initialize MyFilter.

        This filter allows loggers or handlers to log just a specific level.
        kwargs must have levels argument with a list of levels allowed to log.
        """
        self.levels = kwargs.get('levels', [])
        super(LevelFilter, self).__init__(name)

    def filter(self, record):
        """Filter record."""
        if record.levelno in self.levels:
            return True
        return False


class ConsoleHandler(logging.StreamHandler):
    """Custom handler for console."""

    def __init__(self, stream, **kwargs):
        """Init object and set level."""
        super(ConsoleHandler, self).__init__(stream)
        self.setLevel(kwargs.pop('level', logging.INFO))
        self.setFormatter(FMT)


class FileHandler(logging.FileHandler):
    """Custom handler for File."""

    def __init__(self, *args, **kwargs):
        """Init object and set level."""
        self.setLevel(kwargs.pop('level', logging.INFO))
        self.setFormatter(FMT)
        super(FileHandler, self).__init__(*args, **kwargs)
