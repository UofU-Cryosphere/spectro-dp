from pathlib import PurePath

import pytest


@pytest.fixture(scope='session')
def test_data_path():
    return PurePath(__file__).with_name('data')
