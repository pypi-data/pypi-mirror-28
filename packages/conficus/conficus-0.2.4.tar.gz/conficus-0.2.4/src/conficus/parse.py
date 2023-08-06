# pylint: disable=unused-argument
import re
from functools import wraps
from collections import OrderedDict


class FicusDict(OrderedDict):
    '''
    FicusDict is an override of standard dictionary
    to allow dot-named access to nested dictionary
    values.

    The standard nested call:

        config['parent']['child']

    can also be accessed as:

        config['parent.child']

    '''
    def get(self, key, default=None):
        try:
            return self[key]
        except KeyError:
            return default

    def __getitem__(self, key):
        if '.' not in key:
            return super(FicusDict, self).__getitem__(key)
        segments = key.split('.')
        end = self
        for seg in segments:
            end = super(FicusDict, end).__getitem__(seg)
        return end

    def __contains__(self, key):
        if '.' not in key:
            return super(FicusDict, self).__contains__(key)
        segments = key.split('.')
        end = self
        contains = False
        for seg in segments:
            contains = super(FicusDict, end).__contains__(seg)
            if not contains:
                return contains
            end = super(FicusDict, end).__getitem__(seg)
        return contains

    def walk_values(self):
        _values = []

        def _recurse(section, v):
            for val in super(FicusDict, section).values():
                if isinstance(val, FicusDict):
                    _recurse(val, v)
                if isinstance(val, ConfigValue):
                    v.append(val)

        _recurse(self, _values)

        return _values


def matcher(regex):
    '''
    Wrapper around a regex that always returns the
    group dict if there is a match.

    This requires that all regex have named groups.

    '''
    rx = re.compile(regex, re.I)

    # pylint: disable=inconsistent-return-statements
    def _matcher(line):
        m = rx.match(line)
        if m:
            return m.groupdict()

    return _matcher


def substituter(regex, sub):
    rx = re.compile(regex, re.I)

    def _substituter(line):
        line = rx.sub(sub, line)
        return line

    return _substituter


class ConfigValue(object):

    def __init__(self, initial_value):
        self.raw_value = [initial_value]
        self.end_value = None

    def add(self, value):
        self.raw_value.append(value)

    @property
    def multiline(self):
        return len(self.raw_value) > 1

    @property
    def value(self):
        if self.multiline:
            return '\n'.join(self.raw_value)
        #if self.raw_value:
        return str(self.raw_value[0])

    def __deepcopy__(self, memo):
        return self.end_value

# pylint: disable=too-few-public-methods
class parser(object):
    '''
    A decorator that wraps common functioning of
    our parser functions.

    '''
    def __init__(self, rxstr):
        self.regex = matcher(rxstr)

    def __call__(self, func):

        @wraps(func)
        def _parser(line, parm):
            match = self.regex(line)
            if match:
                return func(match, line, parm)
            return line

        return _parser


@parser(r'^\[(?P<section>[^\]]+)\] *$')
def parse_section(match, line, parm):
    '''
    Any line that begins with "[" and ends with "]"
    is considered a section.

    '''
    section_name = match['section'].strip()
    section_heirarchy = section_name.split('.')
    section_dict = parm['config']
    for section in section_heirarchy:
        section_dict = section_dict.setdefault(section, FicusDict())
    parm['current_section'] = section_dict
    return None


@parser(r'^ *(?P<key>[A-Za-z0-9_\-\./\|]+)( ?= ?|: )(?P<value>.*)$')
def parse_option(match, line, parm):
    '''
    An option is any line that begins with a `name` followed
    by an equals sign `=` followed by some value:

        name = 12
        name.subject = 12
        name/subject = 12
        name-subject = 12
        name|subject = 12
        name.subject1 = 12
        Name.Subject3 = 12

    '''
    key = match['key'].strip()
    value = match['value']
    cv = ConfigValue(value)
    parm['current_section'][key] = cv
    parm['current_option'] = cv
    return None


@parser(r'^    *(?P<value>[^#;].*)$')
def parse_multiline_opt(match, line, parm):
    '''
    Any line that is indented with 3 or more spaces is
    considered to be a continuation of the previous
    option value.

    '''
    if parm['current_option'] is not None:
        parm['current_option'].add(match['value'])
    return None


@parser(r'^ *(#|;)(?P<comment>.*)$')
def parse_comment(match, line, parm):
    '''
    Currently we're not handling comments.

    '''
    return None


def parse_unknown(line, parm):
    '''
    Any unmatched lines are ignored.

    '''
    return None


def parse(config_lines):
    '''
    `config_lines` is expected to be a list of strings.
    which will be parsed into sections and key values.

    '''
    parsers = (parse_option,
               parse_multiline_opt,
               parse_section,
               parse_comment,
               parse_unknown)

    config = FicusDict()

    parm = {
        'config': config,
        'current_section': config,
        'current_option': None,
    }

    rmv_crlf = substituter(r'[\r\n]', '')

    while config_lines:

        line = rmv_crlf(config_lines.pop(0))

        for _parser in parsers:
            line = _parser(line, parm)

            if line is None:
                break

    return config
