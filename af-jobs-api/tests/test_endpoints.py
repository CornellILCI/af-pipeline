import json
import uuid

import pytest
from af_requests.models import Request

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
        "dataSourceUrl": "foo",
        "dataSourceAccessToken": "test-token",
        "crop": "rice",
        "institute": "IRRI",
        "analysisType": "ANALYZE",
        "experimentIds": [],
        "occurrenceIds": [],
        "traitIds": [],
        "analysisObjectivePropertyId": None,
        "analysisConfigPropertyId": None,
        "expLocAnalysisPatternPropertyId": None,
        "configFormulaPropertyId": None,
        "configResidualPropertyId": None,
    }


@pytest.fixture
def correct_request():
    return {
        "dataSource": "EBS",
        "dataSourceUrl": "foo",
        "dataSourceAccessToken": "test-token",
        "crop": "rice",
        "institute": "IRRI",
        "analysisType": "ANALYZE",
        "experimentIds": ["1", "2"],
        "occurrenceIds": ["3", "4"],
        "traitIds": ["5", "6"],
        "analysisObjectivePropertyId": "123",
        "analysisConfigPropertyId": "234",
        "expLocAnalysisPatternPropertyId": "456",
        "configFormulaPropertyId": "789",
        "configResidualPropertyId": "111",
    }


def test_empty_request(client, session, empty_request):
    resp = client.post("/v1/requests", json=empty_request)
    assert resp.status_code == 400

    json_response = json.loads(resp.get_data(as_text=True))
    assert str(json_response["errorMsg"]).startswith("11 validation errors")


def test_incorrect_json_request(client, session, incorrect_request):
    resp = client.post("/v1/requests", json=incorrect_request)

    assert resp.status_code == 400
    json_response = json.loads(resp.get_data(as_text=True))
    assert str(json_response["errorMsg"]).startswith("11 validation errors")


def test_incorrect_datasource_datatype(client, session, incorrect_request_2):
    resp = client.post("/v1/requests", json=incorrect_request_2)

    assert resp.status_code == 400
    json_response = json.loads(resp.get_data(as_text=True))
    assert json_response.get("errorMsg")
    assert "value is not a valid enumeration member; permitted: 'EBS', 'BRAPI'" in json_response["errorMsg"]


def test_supposedly_correct_request(client, session, app, correct_request, mocker):
    mock = mocker.MagicMock()
    mocker.patch("celery_util.send_task", mock)

    resp = client.post("/v1/requests", json=correct_request)

    assert resp.status_code == 201

    mock.assert_called()
    kwargs = mock.call_args.kwargs
    assert kwargs.get("process_name") == "analyze"

    # check that the content passed has a 'processId' added
    reqid = kwargs.get("args")[0]
    content = kwargs.get("args")[1]
    assert reqid
    assert content.get("dataSource") == "EBS"
    assert content.get("crop") == "rice"

    # check the response
    resp_json = json.loads(resp.get_data(as_text=True))
    print(resp_json)
    assert resp_json.get("requestId")
    assert resp_json.get("analysisType") == "ANALYZE"
    assert resp_json.get("status") == "PENDING"
    assert resp_json.get("crop") == "rice"
    assert resp_json.get("institute") == "IRRI"
    assert resp_json.get("createdOn")
    assert "modifiedOn" in resp_json  # modifiedOn would be None so this is just a key check


def test_get_request_not_found(client, session):
    resp = client.get("/v1/requests/foo")
    assert resp.status_code == 404

def test_get_analysis_type(client, session):
    resp = client.get("/v1/analysis-type")
    
    assert resp.status_code == 200
    respBody=json.loads(resp.get_data(as_text=True))
    assert len(respBody['response']) > 0



def test_get_request_found(client, db, session):
    test_id = str(uuid.uuid4())
    request = Request(uuid=test_id)
    db.session.add(request)
    db.session.commit()

    resp = client.get(f"/v1/requests/{test_id}")

    assert resp.status_code == 200


def test_get_property(client, db, session):
    resp = client.get("/v1/properties")
    assert resp.status_code == 400

    resp2 = client.get("/v1/properties?propertyRoot=trait_pattern")
    assert resp2.status_code == 200

    
def test_get_datasources(client, session):
    resp = client.get("/v1/datasources")
    assert resp.status_code == 200
