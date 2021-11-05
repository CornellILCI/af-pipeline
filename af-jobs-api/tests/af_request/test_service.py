from af_request import api_models


def test_query(session, af_requests):

    from af_request import service

    query_params = api_models.AnalysisRequestListQueryParameters()
    test_requests = service.query(query_params)

    assert len(test_requests) == len(af_requests)

    # Filter by requestor id and expect 1 result
    expected_request = af_requests[0]

    print(expected_request.requestor_id)
    print(expected_request.uuid)
    print(af_requests[1].requestor_id)
    print(af_requests[1].uuid)

    query_params = api_models.AnalysisRequestListQueryParameters(requestorId=expected_request.requestor_id)

    test_requests = service.query(query_params)
    assert len(test_requests) == 1
    assert test_requests[0].uuid == expected_request.uuid

    # Filter to get empty result
    query_params = api_models.AnalysisRequestListQueryParameters(requestorId="noExistentId")
    test_requests = service.query(query_params)
    assert len(test_requests) == 0


def test_get_by_id(session, af_request):

    from af_request import service

    print(af_request)
    test_request = service.get_by_id(af_request.uuid)

    assert test_request.id == af_request.id
    assert test_request.uuid == af_request.uuid


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
