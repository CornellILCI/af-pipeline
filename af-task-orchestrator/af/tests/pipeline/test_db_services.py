from af.pipeline import db

from af.tests import factories


def test_get_variance_by_source(dbsession, variance):

    assert db.services.query_variance(dbsession) is not None


def test_get_variance_by_source_returns_variance(dbsession, variance):

    variances = db.services.query_variance(dbsession)

    assert type(variances[0]) == db.models.Variance


def test_get_variance_job_id_filter_length(dbsession, variances):

    output_variances = db.services.query_variance(dbsession, job_id=variances[0].job_id)

    assert len(output_variances) == 1


def test_get_variance_job_id_filter(dbsession, variances):

    output_variances = db.services.query_variance(dbsession, job_id=variances[0].job_id)

    assert output_variances[0].job_id == variances[0].job_id


def test_get_variance_job_id_source_filter_length(dbsession, variances):

    output_variances = db.services.query_variance(dbsession, job_id=variances[1].job_id, source=variances[1].source)

    assert len(output_variances) == 1


def test_get_variance_by_job_id_source_filter(dbsession, variances):

    output_variances = db.services.query_variance(dbsession, job_id=variances[1].job_id, source=variances[1].source)

    assert output_variances[0].source == variances[1].source


def test_get_variance_empty_result(dbsession, variances):

    output_variances = db.services.query_variance(dbsession, job_id=variances[2].job_id + 2)

    assert len(output_variances) == 0
