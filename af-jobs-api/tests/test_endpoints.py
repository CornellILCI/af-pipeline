def test_create_request(client, session):

    resp = client.post("/requests")

    assert resp.status_code == 400



def test_get_request(client, session):

    resp = client.get("/requests/foo")

    assert resp.status_code == 400