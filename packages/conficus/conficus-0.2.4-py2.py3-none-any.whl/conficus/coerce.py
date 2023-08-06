import copy
from itertools import chain
from datetime import datetime
from .parse import matcher, substituter


def coerce_single_line(value, *coercers):
    # the match object here may not always
    # return the same thing -
    # TODO: fix this - sometimes it will be a regex matcher
    # that returns a groupdict or else it might be a different
    # function....
    for match, convert in chain(*coercers):
        m = match(value)

        if isinstance(m, dict):
            value = m.get('value', value)
        if m:
            return convert(value)
    # this should never return, but is here for safety
    return value  # pragma: no cover


def coerce_bool(value):
    if value.lower() in ('true', 'yes', 'y', 't'):
        return True
    return False


def coerce_datetime(date_fmt):
    def _coerce_datetime(value):
        return datetime.strptime(value, date_fmt)
    return _coerce_datetime


def coerce_str(value):
    return value.strip('"')

def coerce_none(value):
    return None


simple_coercers = [
    (matcher(r'^(?P<value> +)$'), coerce_none),
    (matcher(r'^(?P<value>)$'), coerce_none),
    (matcher(r'^(?P<value>\d+)$'), int),
    (matcher(r'^(?P<value>\d+\.\d+)$'), float),
    (matcher(r'^(?P<value>(true|false|yes|no|y|n|t|f))\s*$'),
     coerce_bool),
    (matcher(r'^(?P<value>\d{4}-\d\d-\d\dT\d\d:\d\d:\d\d)\s*$'),
     coerce_datetime('%Y-%m-%dT%H:%M:%S')),
    (matcher(r'^(?P<value>\d{4}-\d\d-\d\d)\s*$'),
     coerce_datetime('%Y-%m-%d')),
    (matcher(r'^(?P<value>\d\d:\d\d:\d\d)\s*$'),
     coerce_datetime('%H:%M:%S')),
    (matcher(r'^(?P<value>("{1,3})?.*("{1,3})?)\s*$'),
     coerce_str)]


def match_iterable(start_bracket, end_bracket):

    def _match_iterable(value):
        return value.startswith(start_bracket) and value.endswith(end_bracket)

    return _match_iterable


def coerce_iterable(use_tuple=False):

    def _coerce_iterable(value):
        value = value[1:-1]

        if not value and use_tuple is False:
            return []
        elif not value:
            return tuple()

        iterable = [coerce_single_line(v.strip(), simple_coercers) for v
                    in value.split(',')]
        if use_tuple:
            iterable = tuple(iterable)

        return iterable

    return _coerce_iterable


match_single_line_list = match_iterable('[', ']')
match_single_line_tuple = match_iterable('(', ')')

coerce_single_line_list = coerce_iterable()
coerce_single_line_tuple = coerce_iterable(use_tuple=True)


list_coercers = [(match_single_line_list, coerce_single_line_list),
                 (match_single_line_tuple, coerce_single_line_tuple)]


def match_multiline_list(value):
    return value[0].startswith('[') and value[-1].endswith(']')


def match_multiline_str(value):
    return value[0].startswith('"""') and value[-1].endswith('"""')


def coerce_single_line_str(value):
    '''
    Multiline strings have two options:

        1. Preserve new lines with the back slash:

            value = """A new value \
                and something else \
                to boot.
            """

            A new value
            and something else
            to boot.

        2. Preserve left spacing with the pipe:

            value = """A new value \
                |   it's true."""

           A new value
              it's true.

    '''


sub_new_line = substituter(r'[\r\n]+$', '')
sub_line_ending = substituter(r'\\ *$', '\n')
sub_line_beginning = substituter(r'^ *\|', '')


def coerce_multiline(value, *coercers):

    if match_multiline_list(value):
        value[0] = value[0].lstrip('[')
        value[-1] = value[-1].rstrip(']')
        value = [v.strip().rstrip(',') for v in value]
        return [coerce_single_line(v, list_coercers, simple_coercers, *coercers)
                for v in value if v]

    elif match_multiline_str(value):
        value[0] = value[0].lstrip('"')
        value[-1] = value[-1].rstrip('"')
        # remove blank first line
        if value[0].strip() == '':
            value.pop(0)
        value = [sub_new_line(v) for v in value]
        value = [sub_line_ending(v) for v in value]
        value = [sub_line_beginning(v) for v in value]
        return ''.join(value)

    else:
        return '\n'.join(value)


def coerce(config, *coercers):

    for cfg_obj in config.walk_values():
        if cfg_obj.multiline:
            cfg_obj.end_value = coerce_multiline(cfg_obj.raw_value, *coercers)
        else:
            cfg_obj.end_value = coerce_single_line(cfg_obj.value,
                                                   list_coercers,
                                                   simple_coercers,
                                                   *coercers)
    return copy.deepcopy(config)
