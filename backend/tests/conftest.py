import pytest
from mongoengine import connect
from mongoengine.connection import disconnect
import app
import model
import copy
import test_data


@pytest.fixture
def db():
    '''
    Provides a mock database, clearing it before and after use.
    '''
    disconnect()
    connect('mongoenginetest', host='mongomock://localhost')
    model.Item.objects().delete()
    yield None
    model.Item.objects().delete()


@pytest.fixture
def client():
    '''
    Provides a test client (acting as the frontend making requests).
    '''
    app.app.config['TESTING'] = True
    client = app.app.test_client()
    return client


@pytest.fixture
def nonexistent_item(db):
    '''
    Provides an Item that does not exist in the database
    '''
    test_item = test_data.valid_items[0]
    assert model.Item.objects(upc=test_item.upc).count() == 0, \
        'Test item was not cleared from database after previous test'
    return test_item


@pytest.fixture
def existing_item(db, nonexistent_item):
    '''
    Provides an Item that exists in the database for testing
    '''
    item = copy.deepcopy(nonexistent_item)
    item.save()
    return item
