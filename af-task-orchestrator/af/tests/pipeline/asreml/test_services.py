from af.pipeline import asreml

def test_process_result_returns_asreml_result(dbsession):

    assert type(asreml.services.process_asreml_result(dbsession, 1, "")) == type(AsremlResult)
