from pathlib import Path
import pytest
import conficus


CWD = Path().resolve()
DOCS = Path(CWD, 'test', 'samples')
PATHS = {
    'config': Path(DOCS, 'config.txt'),
    'coerce': Path(DOCS, 'config_coerce.txt'),
    'multiline': Path(DOCS, 'config_multiline.txt'),
    'toml': Path(DOCS, 'example-v0.4.0.toml')
}


@pytest.fixture
def cfg_pth():
    return PATHS


@pytest.fixture
def raw_cfg():
    lines = conficus.read_config(str(PATHS['config']))
    return conficus.parse(lines)


@pytest.fixture
def coerce_cfg():
    lines = conficus.read_config(str(PATHS['coerce']))
    return conficus.parse(lines)


@pytest.fixture
def multiline_cfg():
    lines = conficus.read_config(str(PATHS['multiline']))
    return conficus.parse(lines)
