import json
import uuid

import pytest
from af_request.models import Analysis, Request


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
        "experiments": [],
        "occurrences": [],
        "traits": [],
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
        "experiments": [{"experimentId": "10", "experimentName": "expt1"}],
        "occurrences": [{"occurrenceId": "10", "occurrenceName": "occur1"}],
        "traits": [{"traitId": "1", "traitName": "trait1"}, {"traitId": "2", "traitName": "trait2"}],
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
    assert str(json_response["errorMsg"]).startswith("10 validation errors")


def test_incorrect_json_request(client, session, incorrect_request):
    resp = client.post("/v1/requests", json=incorrect_request)

    assert resp.status_code == 400
    json_response = json.loads(resp.get_data(as_text=True))
    assert str(json_response["errorMsg"]).startswith("10 validation errors")


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
    assert "modifiedOn" not in resp_json


def test_get_request_not_found(client, session):
    resp = client.get("/v1/requests/foo")
    assert resp.status_code == 404


def test_get_request_found(client, db, session, analysis):

    resp = client.get(f"/v1/requests/{analysis.request.uuid}")

    assert resp.status_code == 200


def test_get_by_id_formula_fetched(client, session, analysis):

    from af_request import service

    resp = client.get(f"/v1/requests/{analysis.request.uuid}")

    resp_content = resp.get_json()
    result = resp_content["result"]

    assert "configFormulaProperty" in result
    assert result.get("configFormulaProperty").get("propertyId") == str(analysis.formula.id)


def test_get_by_id_analysis_objective_fetched(client, session, analysis):

    from af_request import service

    resp = client.get(f"/v1/requests/{analysis.request.uuid}")

    resp_content = resp.get_json()
    result = resp_content["result"]

    assert "analysisObjectiveProperty" in result
    assert result.get("analysisObjectiveProperty").get("propertyId") == str(analysis.analysis_objective.id)


def test_get_by_id_analysis_config_fetched(client, session, analysis):

    from af_request import service

    resp = client.get(f"/v1/requests/{analysis.request.uuid}")

    resp_content = resp.get_json()
    result = resp_content["result"]

    assert "analysisConfigProperty" in result
    assert result.get("analysisConfigProperty").get("propertyId") == str(analysis.model.id)


def test_get_by_id_exploc_property_fetched(client, session, analysis):

    from af_request import service

    resp = client.get(f"/v1/requests/{analysis.request.uuid}")

    resp_content = resp.get_json()
    result = resp_content["result"]

    assert "expLocAnalysisPatternProperty" in result
    assert result.get("expLocAnalysisPatternProperty").get("propertyId") == str(analysis.exp_loc_pattern.id)


def test_get_by_id_residual_fetched(client, session, analysis):

    from af_request import service

    resp = client.get(f"/v1/requests/{analysis.request.uuid}")

    resp_content = resp.get_json()
    result = resp_content["result"]

    assert "configResidualProperty" in result
    assert result.get("configResidualProperty").get("propertyId") == str(analysis.residual.id)


def test_get_by_id_status_message_mapped(client, session, analysis):

    from af_request import service

    resp = client.get(f"/v1/requests/{analysis.request.uuid}")

    resp_content = resp.get_json()
    result = resp_content.get("result")

    assert "statusMessage" in result


def test_get_by_id_status_message_content(client, session, analysis):

    from af_request import service

    resp = client.get(f"/v1/requests/{analysis.request.uuid}")

    resp_content = resp.get_json()
    result = resp_content.get("result")

    assert result.get("statusMessage") == analysis.request.msg


def test_get_by_id_jobs_found(client, session, analysis):

    from af_request import service

    resp = client.get(f"/v1/requests/{analysis.request.uuid}")

    resp_content = resp.get_json()
    result = resp_content.get("result")

    assert "jobs" in result


def test_get_by_id_jobs_mapped(client, session, analysis):

    from af_request import service

    resp = client.get(f"/v1/requests/{analysis.request.uuid}")

    resp_content = resp.get_json()
    result = resp_content.get("result")

    jobs = result.get("jobs")
    job1 = jobs[0]

    assert str(analysis.jobs[0].id) == job1.get("jobId")


def test_get_by_id_experiments_found(client, session, analysis):

    from af_request import service

    resp = client.get(f"/v1/requests/{analysis.request.uuid}")

    resp_content = resp.get_json()
    result = resp_content.get("result")

    assert "experiments" in result


def test_get_by_id_experiments_found(client, session, analysis):

    from af_request import service

    resp = client.get(f"/v1/requests/{analysis.request.uuid}")

    resp_content = resp.get_json()
    result = resp_content.get("result")

    assert result.get("experiments") == analysis.analysis_request_data.get("experiments")


def test_get_by_id_traits_found(client, session, analysis):

    from af_request import service

    resp = client.get(f"/v1/requests/{analysis.request.uuid}")

    resp_content = resp.get_json()
    result = resp_content.get("result")

    assert "traits" in result


def test_get_by_id_traits_found(client, session, analysis):

    from af_request import service

    resp = client.get(f"/v1/requests/{analysis.request.uuid}")

    resp_content = resp.get_json()
    result = resp_content.get("result")

    assert result.get("traits") == analysis.analysis_request_data.get("traits")
