def test_list(session, af_requests):

    from af_request import service

    test_requests = service.get_all()

    assert len(test_requests) == len(af_requests)
