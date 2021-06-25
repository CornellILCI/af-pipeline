import io

from pipeline.asreml.services import process_asreml_result
from pipeline.db.models import ModelStat, Variance


def test_simple_test_1(dbsession, sample_asreml_result_string_1):
    # create test stream from sample_asreml_result_string_1
    sample_stream = io.StringIO(sample_asreml_result_string_1)
    sample_job_id = 123

    process_asreml_result(dbsession, sample_job_id, sample_stream)

    # check objects saved
    assert dbsession.query(Variance.id).count() == 3
    assert dbsession.query(ModelStat.id).count() == 1
