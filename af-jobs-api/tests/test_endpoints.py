import uuid

from database import Request


def test_create_request(client, session):

    resp = client.post("/requests")

    assert resp.status_code == 400


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
git sta