import json

import pytest


def test_get_analysis_type(client, session):
    resp = client.get("/v1/analysis-type")

    assert resp.status_code == 200
    respBody = json.loads(resp.get_data(as_text=True))
    assert len(respBody["response"]) > 0


def test_get_property(client, db, session):
    resp = client.get("/v1/properties")
    assert resp.status_code == 400

    resp2 = client.get("/v1/properties?propertyRoot=trait_pattern")
    assert resp2.status_code == 200


def test_get_datasources(client, session):
    resp = client.get("/v1/datasources")
    assert resp.status_code == 200
