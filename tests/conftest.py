import sys
import os

import pytest

collect_ignore = ['setup.py', 'demo_waterfall.py']

ASYNC_AVAILABLE = sys.version_info.major >= 3
if sys.version_info.major == 3:
    ASYNC_AVAILABLE = sys.version_info.minor >= 5
if not ASYNC_AVAILABLE:
    collect_ignore.append('test_aio.py')

def is_travisci():
    return all([os.environ.get(key) == 'true' for key in ['CI', 'TRAVIS']])

@pytest.fixture(autouse=True)
def librtlsdr_override(monkeypatch):
    if not is_travisci():
        return
    import testlibrtlsdr
    for attr in ['p_rtlsdr_dev', 'librtlsdr', 'rtlsdr_read_async_cb_t']:
        lib_attr = '.'.join(['rtlsdr', 'rtlsdr', attr])
        override = getattr(testlibrtlsdr, attr)
        monkeypatch.setattr(lib_attr, override)

@pytest.fixture(params=[True, False])
def use_numpy(request, monkeypatch):
    if not request.param:
        monkeypatch.setattr('rtlsdr.rtlsdr.has_numpy', False)
    return request.param

@pytest.fixture
def sdr_cls():
    from rtlsdr.rtlsdr import RtlSdr
    return RtlSdr

@pytest.fixture
def rtlsdrtcp():
    from rtlsdr import rtlsdrtcp
    return rtlsdrtcp

@pytest.fixture
def rtlsdraio():
    from rtlsdr import rtlsdraio
    return rtlsdraio
