def test_list(db, af_requests):

    from af_request import service

    test_requests = service.get_all()
    
    print(test_requests)

    assert len(test_requests) == 3
