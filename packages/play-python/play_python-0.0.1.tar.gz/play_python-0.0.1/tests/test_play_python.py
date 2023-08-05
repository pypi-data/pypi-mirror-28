#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""Tests for `play_python` package."""

import pytest


@pytest.mark.parametrize('expression', [
    '200 == 200',
    '200 != 404 and 10>0',
    'variables["foo"] == "baz"',
    '"foo" in variables',
    'len([1]) == 1',
    '[1][0] == 1',
    'len(list(variables.items())) == 1',
    'variables["foo"].upper() == "BAZ"',
    'match(r"^([0-9]*)-data", "123-data")',
    'match(r"^([0-9]*)-data", "123-data").group(1) == "123"'
])
def test_assertion(expression):
    import mock
    mock_engine = mock.MagicMock()
    mock_engine.variables = {'foo': 'baz'}
    from play_python import providers
    provider = providers.PythonProvider(mock_engine)
    assert provider.engine is mock_engine
    provider.command_assert({
        'provider': 'python',
        'type': 'assert',
        'expression': expression
    })


def test_assertion_ko():
    import mock
    mock_engine = mock.MagicMock()
    mock_engine.variables = {'foo': 'baz'}
    from play_python import providers
    provider = providers.PythonProvider(mock_engine)
    assert provider.engine is mock_engine
    with pytest.raises(AssertionError):
        provider.command_assert({
            'provider': 'python',
            'type': 'assert',
            'expression': '200 == 404'
        })


@pytest.mark.parametrize('expression', [
    'open("/etc/passwd", "r")',
    'open',
    'import os',
    '__file__',
    '__file__',
    '__builtins__.__dict__["bytes"]',
    '__builtins__.__dict__["bytes"] = "pluto"',
    'prova = lambda: 1',
    'os = 1',
])
def test_assertion_bad(expression):
    import mock
    mock_engine = mock.MagicMock()
    mock_engine.variables = {'foo': 'baz'}
    from play_python import providers
    provider = providers.PythonProvider(mock_engine)
    assert provider.engine is mock_engine
    with pytest.raises(Exception):
        provider.command_assert({
            'provider': 'python',
            'type': 'assert',
            'expression': expression
        })


def test_store_variable():
    import mock
    mock_engine = mock.MagicMock()
    mock_engine.variables = {'foo': 'baz'}
    from play_python import providers
    provider = providers.PythonProvider(mock_engine)
    assert provider.engine is mock_engine
    provider.command_store_variable({
        'provider': 'python',
        'type': 'store_variable',
        'expression': '1+1',
        'name': 'sum2'
    })
    assert 'sum2' in mock_engine.variables
    assert mock_engine.variables['foo'] == 'baz'
    assert mock_engine.variables['sum2'] == 2


def test_exec():
    import mock
    mock_engine = mock.MagicMock()
    mock_engine.variables = {'foo': 'baz'}
    from play_python import providers
    provider = providers.PythonProvider(mock_engine)
    assert provider.engine is mock_engine
    assert provider.command_exec({
        'provider': 'python',
        'type': 'exec',
        'expression': '1+1',
        }) == 2


@pytest.mark.parametrize('expression', [
    'variable == 200',
])
def test_assertion_kwargs(expression):
    import mock
    mock_engine = mock.MagicMock()
    mock_engine.variables = {'foo': 'baz'}
    assert 'variable' not in mock_engine.variables
    from play_python import providers
    provider = providers.PythonProvider(mock_engine)
    assert provider.engine is mock_engine
    provider.command_assert({
        'provider': 'python',
        'type': 'assert',
        'expression': expression
        },
        variable=200)
    assert 'variable' not in mock_engine.variables


def test_sleep():
    import mock
    mock_engine = mock.MagicMock()
    mock_engine.variables = {}
    from play_python import providers
    provider = providers.PythonProvider(mock_engine)
    assert provider.engine is mock_engine
    from datetime import (
        datetime,
        timedelta,
    )
    now = datetime.now()
    provider.command_sleep({
        'provider': 'python',
        'type': 'sleep',
        'seconds': 2
    })
    now_now = datetime.now()
    expected_date = now + timedelta(milliseconds=2000)
    assert now_now >= expected_date
