from af_request import api_models


def test_query(session, analyses):

    from af_request import service

    query_params = api_models.AnalysisRequestListQueryParameters()
    actual_analyses = service.query(query_params)

    assert len(analyses) == len(actual_analyses)

    expected_request = analyses[0].request
    query_params = api_models.AnalysisRequestListQueryParameters(requestorId=expected_request.requestor_id)

    actual_analyses = service.query(query_params)
    assert len(actual_analyses) == 1
    assert actual_analyses[0].request.uuid == expected_request.uuid

    # Filter to get empty result
    query_params = api_models.AnalysisRequestListQueryParameters(requestorId="noExistentId")
    actual_analyses = service.query(query_params)
    assert len(actual_analyses) == 0


def test_get_by_id(session, analysis):

    from af_request import service

    actual_analysis = service.get_by_id(analysis.request.uuid)

    assert analysis.id == actual_analysis.id
    assert analysis.request.uuid == actual_analysis.request.uuid


def test_submit(session, af_request_parameters, celery_send_task):

    from af_request import service

    actual_analysis_submitted = service.submit(af_request_parameters)
    actual_analysis_request = actual_analysis_submitted.request

    celery_send_task.assert_called()

    task_kwargs = celery_send_task.call_args.kwargs
    assert task_kwargs.get("process_name") == "analyze"

    reqid = task_kwargs.get("args")[0]
    content = task_kwargs.get("args")[1]

    assert reqid == actual_analysis_request.uuid
    assert content.get("dataSource") == af_request_parameters.dataSource
    assert content.get("crop") == af_request_parameters.crop
