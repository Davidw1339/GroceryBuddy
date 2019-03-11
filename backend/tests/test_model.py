import pytest
import model
import test_data
import copy


def test_model_loads():
    assert True


def test_valid_items(db):
    for item in test_data.valid_items:
        copy.deepcopy(item).save()
    result = model.Item.objects()
    assert len(result) == len(test_data.valid_items)


def test_invalid_items():
    for item in test_data.invalid_items:
        try:
            item.save()
            assert False
        except Exception:
            pass
