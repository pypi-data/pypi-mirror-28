################################################################
# pp.core2 - Produce & Publish
# (C) 2013, ZOPYX Limited, www.zopyx.com
################################################################

import tempfile
from pp.core2.resources_registry import _resources_registry
from pp.core2.resources_registry import registerResource
from pp.core2.resources_registry import getResource
from pp.core2.resources_registry import getResourceNames

import pytest

def test_empty():
    assert len(getResourceNames()) == 0
    with pytest.raises(KeyError):
        getResource('foo')

def test_insert():
    _resources_registry.clear()
    registerResource('foo', tempfile.gettempdir())
    resource = getResource('foo')
    assert getResourceNames() == ['foo']

def test_insert_twice():
    _resources_registry.clear()
    registerResource('foo', tempfile.gettempdir())
    with pytest.raises(KeyError):
        registerResource('foo', tempfile.gettempdir())
