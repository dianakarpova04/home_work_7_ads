"""
Modules for testing API
"""
from fastapi.testclient import TestClient

from app.main import app

client = TestClient(app)


def test_hello():
    """
    Def for testing start API request
    :return: assert nothing if everything is correct
    """
    # Test for starting request
    response = client.get('/')
    assert response.status_code == 200
    assert 'application/json' in response.headers['content-type']
    assert response.json()["message"] == "Hello! This is the fraud detector."


def test_get_cost():
    """
    Def for testing API request for each error cost
    :return: assert nothing if everything is correct
    """
    # Test for getting cost of false-positive error
    response = client.get("/cost/false-positive")
    assert response.status_code == 200
    assert response.json() == {"cost": 10000}

    # Test for getting cost of false-negative error
    response = client.get("/cost/false-negative")
    assert response.status_code == 200
    assert response.json() == {"cost": 75000}

    # # Test for getting cost of non-existent-error
    # response = client.get("/cost/non-existent-error")
    # assert response.status_code == 404
    # assert response.json() == {"detail": "Error type not found"}


def test_get_loss():
    """
    Def for testing losses for each baseline
    :return: assert nothing if everything is correct
    """
    # Test for an existing baseline 'constant-clean'
    response = client.get("/loss/constant-clean")
    assert response.status_code == 200
    assert "losses" in response.json()

    # Test for an existing baseline 'constant-fraud'
    response = client.get("/loss/constant-fraud")
    assert response.status_code == 200
    assert "losses" in response.json()

    # Test for an existing baseline 'first-hypothesis'
    response = client.get("/loss/first-hypothesis")
    assert response.status_code == 200
    assert "losses" in response.json()


def test_post_predict():
    """
    Test for prediction based on some text and baseline
    :return: assert nothing if everything is correct
    """
    # Test for correct prediction based on some text
    response = client.post("/predict/constant-clean",
                           json={
                               "text": "мы украдем ваши денежки"  # noqa
                           })
    assert response.status_code == 200
    assert response.json()['prediction'] == "clean"  # super cool prediction


def test_get_latest_entry():
    """
    Test for last entry in DB
    :return: assert nothing if everything is correct
    """
    # Test for latest_entry for constant-clean
    response = client.get("/get_latest_entry/constant-clean")
    assert response.status_code == 200

    # Test for latest_entry for constant-fraud
    response = client.get("/get_latest_entry/constant-fraud")
    assert response.status_code == 200

    # Test for latest_entry for first-hypothesis
    response = client.get("/get_latest_entry/first-hypothesis")
    assert response.status_code == 200

    # Test for latest_entry for non-existent-baseline
    response = client.get("/get_latest_entry/non-existent-baseline")
    assert response.status_code == 200
    assert response.json()["message"] == "No entry found for the specified baseline."  # noqa


def test_get_number_of_entries():
    """
    Test for getting number of prediction in DB
    :return: assert nothing if everything is correct
    """
    # Test for counting each baseline in db
    response = client.get("/get_number_of_entries")
    assert response.status_code == 200
