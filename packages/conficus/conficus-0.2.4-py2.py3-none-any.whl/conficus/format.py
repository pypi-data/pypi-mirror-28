def format_dict(defaults):  # noqa C901

    if not isinstance(defaults, dict):
        raise Exception('Ficus requires a dict to write to file.')

    output = []

    def _recurse(src, parent=''):
        sections = []
        values = []
        for key, val in src.items():
            if isinstance(val, dict):
                sections.append((key, val))
            else:
                values.append((key, val))

        if len(values) > 0:
            output.append('[{}]'.format(parent))

        for key, val in values:
            output.append('{} = {}'.format(key, val))

        for key, val in sections:
            _recurse(val, (parent + '.' + key).strip('.'))

    _recurse(defaults)

    return '\n'.join(output)
