from af.pipeline import db

from af.tests import factories

def test_get_variance_by_source(dbsession, variance):

    assert db.services.get_variance_by_source(dbsession, variance.job_id, "test") is not None


def test_get_variance_by_source_returns_variance(dbsession, variance):

    assert type(db.services.get_variance_by_source(dbsession, variance.job_id, "test")) == db.models.Variance


def test_get_variance_job_id_filter_working(dbsession, variance):

    output_variance = db.services.get_variance_by_source(dbsession, variance.job_id, "test")

    assert variance.job_id == output_variance.job_id


