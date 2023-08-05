import pytest
from datetime import datetime
from collections import OrderedDict
from conficus.format import format_dict


default_config = OrderedDict({
    'section': {
        'value': 'hello',
        'subsection': {
            'value': 'goodbye',
            'three': {
                'repeat': datetime(2017, 5, 28, 10, 10, 10)
            }
        }
    },
    'section.two': {
        'value': 2
    }
})


@pytest.mark.skip(reason="incomplete functionality")
def test_dump_section():
    ini = format_dict(default_config)

    assert ini == ('[section]\n'
                   'value = hello\n'
                   '[section.subsection]\n'
                   'value = goodbye\n'
                   '[section.subsection.three]\n'
                   'repeat = 2017-05-28 10:10:10\n'
                   '[section.two]\n'
                   'value = 2')
