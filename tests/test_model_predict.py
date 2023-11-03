"""
Module with def for test
"""
from app.model_predict import Baseline


def test_prediction():
    """
    Check the result in function
    :return: assert
    """
    predict = Baseline()

    result = predict.prediction('constant-fraud', 'some text')
    assert result == 'fraud'

    result = predict.prediction('constant-clean', 'some text')
    assert result == 'clean'

    result = predict.prediction('first-hypothesis', 'whatsapp')
    assert result == 'fraud'

    result = predict.prediction('first-hypothesis', 'some test')
    assert result == 'clean'
