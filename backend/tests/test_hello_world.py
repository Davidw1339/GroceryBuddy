import pytest


def test_hello_world(client):
    rv = client.get('/')
    assert rv.data.decode('ascii') == 'Hello, Grocery buddies!'
