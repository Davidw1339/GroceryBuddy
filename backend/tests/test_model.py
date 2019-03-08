import model
from mongoengine import connect
from test_data import valid_items, invalid_items
import copy

connect('mongoenginetest', host='mongomock://localhost')


def test_model_loads():
    assert True


def test_valid_items():
    for item in valid_items:
        copy.deepcopy(item).save()
    result = model.Item.objects()
    assert len(result) == len(valid_items)


def test_invalid_items():
    for item in invalid_items:
        try:
            item.save()
            assert False
        except Exception:
            pass
