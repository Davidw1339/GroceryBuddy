import model
import test_data
import copy
import mongoengine.errors as errors
import validation


def test_model_loads():
    '''
    Tests that the Model class loads successfully.
    (fails if "import model" fails)
    '''
    assert True


def test_valid_items(db):
    '''
    Tests adding valid items.
    '''
    for item in test_data.valid_items:
        copy.deepcopy(item).save()
    result = model.Item.objects()
    assert len(result) == len(test_data.valid_items)


def test_invalid_items():
    '''
    Tests adding invalid items.
    '''
    for item in test_data.invalid_items:
        try:
            item.save()
        except errors.ValidationError:
            pass
        except validation.ValidationException:
            pass
