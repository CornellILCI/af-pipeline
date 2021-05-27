import json
import uuid

import pytest
from database import Request

## fixture area
# sample request data


@pytest.fixture
def empty_request():
    return {}


@pytest.fixture
def incorrect_request():
    return {"foo": "bar"}


@pytest.fixture
def incorrect_request_2():
    return {
        "dataSource": "NOT_EBS",
        "dataSourceId": "Some-Datasource-ID",
        "dataType": "NOT_VALID",
        "apiBearerToken": "test-token",
        "processName": "test_process",
    }


@pytest.fixture
def correct_request():
    return {
        "dataSource": "EBS",
        "dataSourceId": "Some-Datasource-ID",
        "dataType": "PHENOTYPE",
        "apiBearerToken": "test-token",
        "processName": "test_process",
    }


def test_empty_request(client, session, empty_request):
    resp = client.post("/requests", json=empty_request)
    assert resp.status_code == 400

    json_response = json.loads(resp.get_data(as_text=True))
    assert json_response["status"] == "error"
    assert json_response["message"][0] == "Empty request."


def test_incorrect_json_request(client, session, incorrect_request):
    resp = client.post("/requests", json=incorrect_request)

    assert resp.status_code == 400
    json_response = json.loads(resp.get_data(as_text=True))
    assert json_response["status"] == "error"
    assert json_response["message"], "Expected content in message attribute"
    assert "dataSource does not exist in the request." in json_response["message"]
    assert "dataSourceId does not exist in the request." in json_response["message"]
    assert "dataType does not exist in the request." in json_response["message"]
    assert "processName does not exist in the request." in json_response["message"]
    assert "token does not exist in the request." in json_response["message"]


def test_incorrect_datasource_datatype(client, session, incorrect_request_2):
    resp = client.post("/requests", json=incorrect_request_2)

    assert resp.status_code == 400
    json_response = json.loads(resp.get_data(as_text=True))
    assert json_response["status"] == "error"
    assert json_response["message"]
    assert "dataSource is not 'EBS' or 'BRAPI'." in json_response["message"]
    assert "dataType is not 'GENOTYPE' or 'PHENOTYPE'." in json_response["message"]


def test_supposedly_correct_request(client, session, app, correct_request, mocker):
    mock = mocker.MagicMock()
    mocker.patch("celery_util.send_task", mock)

    resp = client.post("/requests", json=correct_request)
    assert resp.status_code == 201

    mock.assert_called()
    kwargs = mock.call_args.kwargs
    assert kwargs.get("process_name") == "test_process"

    # check that the content passed has a 'processId' added
    content = kwargs.get("args")[0]
    assert "processId" in content


def test_get_request_not_found(client, session):
    resp = client.get("/requests/foo")
    assert resp.status_code == 404


def test_get_request_found(client, db, session):
    test_id = str(uuid.uuid4())
    request = Request(uuid=test_id)
    db.session.add(request)
    db.session.commit()

    resp = client.get(f"/requests/{test_id}")

    assert resp.status_code == 200


def test_get_datasources(client, session):
    resp = client.get("/datasources")
    assert resp.status_code == 200