from af_request import api_models


def test_query(session, af_requests):

    from af_request import service

    query_params = api_models.AnalysisRequestListQueryParameters()
    test_requests = service.query(query_params)

    assert len(test_requests) == len(af_requests)

    # Filter by requestor id and expect 1 result
    expected_request = af_requests[0]

    query_params = api_models.AnalysisRequestListQueryParameters(requestorId=expected_request.requestor_id)

    test_requests = service.query(query_params)
    assert len(test_requests) == 1
    assert test_requests[0].uuid == expected_request.uuid

    # Filter to get empty result
    query_params = api_models.AnalysisRequestListQueryParameters(requestorId="noExistentId")
    test_requests = service.query(query_params)
    assert len(test_requests) == 0


def test_get_by_id(session, analysis):

    from af_request import service

    actual_analysis = service.get_by_id(analysis.request.uuid)

    assert analysis.id == actual_analysis.id
    assert analysis.request.uuid == actual_analysis.request.uuid

def test_get_by_id_formula_fetched(session, analysis):

    from af_request import service

    actual_analysis = service.get_by_id(analysis.request.uuid)

    assert analysis.formula.id == analysis.formula.id
    assert analysis.formula.name == analysis.formula.name
    assert analysis.formula.statement == analysis.formula.statement

def test_submit(session, af_request_parameters, celery_send_task):

    from af_request import service

    test_request = service.submit(af_request_parameters)

    celery_send_task.assert_called()

    task_kwargs = celery_send_task.call_args.kwargs
    assert task_kwargs.get("process_name") == "analyze"

    reqid = task_kwargs.get("args")[0]
    content = task_kwargs.get("args")[1]

    assert reqid == test_request.uuid
    assert content.get("dataSource") == af_request_parameters.dataSource
    assert content.get("crop") == af_request_parameters.crop
