import io
from tempfile import NamedTemporaryFile

from numpy import save

from af.pipeline.asreml.services import process_asreml_result, process_yhat_result, save_residual_outlier
from af.pipeline.db.models import FittedValues, ModelStat, Prediction, Variance, ResidualOutlier
import json


def test_simple_test_1(dbsession, sample_asreml_result_string_1):
    # create test stream from sample_asreml_result_string_1
    sample_stream = io.StringIO(sample_asreml_result_string_1)
    sample_job_id = 123

    process_asreml_result(dbsession, sample_job_id, sample_stream)

    # check objects saved
    assert dbsession.query(Variance.id).count() == 3
    assert dbsession.query(ModelStat.id).count() == 1
    assert dbsession.query(Prediction.id).count() == 180


def test_asr_not_converged_result(dbsession, sample_asreml_not_converged_result_string):
    # create test stream from sample_asreml_result_string_1
    sample_stream = io.StringIO(sample_asreml_not_converged_result_string)
    sample_job_id = 123

    process_asreml_result(dbsession, sample_job_id, sample_stream)

    # check objects saved
    assert dbsession.query(Variance.id).count() == 0  # there should be no variance objects saved
    assert dbsession.query(ModelStat.id).count() == 1  # model stat should be saved
    assert dbsession.query(Prediction.id).count() == 0  # there should be no prediction objects saved.
    assert dbsession.query(ResidualOutlier.id).count() == 0  # there should be no prediction objects saved.


def test_yhat_parser_service_happy_path(sample_yhat_data_1, dbsession):

    process_yhat_result(dbsession, 1, sample_yhat_data_1)

    # make assertions about what is supposed to be in the database
    assert dbsession.query(FittedValues.id).count() == 2

    record = dbsession.query(FittedValues).filter_by(record=1).first()
    assert record.additional_info  # not empty

    # SQLITE gets the data as string so, we must do a test
    json_data = json.loads(record.additional_info)
    assert json_data.get("RinvRes") == 0.009825

    
def test_save_residual_outlier(sample_res_data_1, dbsession):
    x = dbsession.query(ResidualOutlier.id)  
    tmp = NamedTemporaryFile()
    data = """Residual [section 11, column 9 (of 15), row 19 (of 28)] is  3.70 SD\nResidual [section 11, column 15 (of 15), row 2 (of 28)] is  3.61 SD
"""
    data2 = "STND RES\t30\t12.362\t3.81"

    tmp.write(bytes(data2, 'UTF-8'))
    tmp.seek(0)

    y = save_residual_outlier(dbsession, tmp.name)
    assert dbsession.query(ResidualOutlier.outliers).count() == 0
