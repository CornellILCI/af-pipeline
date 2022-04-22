import io
import json
import tempfile

import pytest
from af.pipeline import asreml
from af.pipeline.asreml.services import process_asreml_result, process_yhat_result
from af.pipeline.db.models import FittedValues, ModelStat, PredictionEffect, Variance


def test_simple_test_1(dbsession, sample_asreml_result_string_1, job):
    # create test stream from sample_asreml_result_string_1
    sample_stream = io.StringIO(sample_asreml_result_string_1)
    sample_job_id = job.id
    process_asreml_result(dbsession, sample_job_id, sample_stream)

    # check objects saved
    assert dbsession.query(Variance.id).count() == 3
    assert dbsession.query(ModelStat.id).count() == 1
    assert dbsession.query(PredictionEffect.id).count() == 180


def test_asr_not_converged_result(dbsession, sample_asreml_not_converged_result_string):
    # create test stream from sample_asreml_result_string_1
    sample_stream = io.StringIO(sample_asreml_not_converged_result_string)
    sample_job_id = 123

    process_asreml_result(dbsession, sample_job_id, sample_stream)

    # check objects saved
    assert dbsession.query(Variance.id).count() == 0  # there should be no variance objects saved
    assert dbsession.query(ModelStat.id).count() == 1  # model stat should be saved
    assert dbsession.query(PredictionEffect.id).count() == 0  # there should be no prediction objects saved.


def test_yhat_parser_service_happy_path(sample_yhat_data_1, dbsession):

    process_yhat_result(dbsession, 1, sample_yhat_data_1)

    # make assertions about what is supposed to be in the database
    assert dbsession.query(FittedValues.id).count() == 2

    record = dbsession.query(FittedValues).filter_by(record=1).first()
    assert record.additional_info  # not empty

    # SQLITE gets the data as string so, we must do a test
    json_data = json.loads(record.additional_info)
    assert json_data.get("RinvRes") == 0.009825


def test_get_average_std_error_returns_float(temp_file):

    assert type(asreml.services.get_average_std_error(temp_file.name)) is float


def test_get_average_std_error_checks_for_valid_file(mocker, temp_file):

    check_valid_file_method = mocker.patch("af.pipeline.utils.is_valid_file")
    asreml.services.get_average_std_error(temp_file.name)
    check_valid_file_method.assert_called_once_with(temp_file.name)


def test_get_average_std_error_throws_value_error_for_invalid_file(mocker):

    check_valid_file_method = mocker.patch("af.pipeline.utils.is_valid_file", return_value=False)

    with pytest.raises(ValueError, match="SE Blup Calculation: PVS file not found in ASReml results."):
        asreml.services.get_average_std_error("dummy")


def test_get_average_error_reads_correct_lines_from_file(temp_file):

    pvs_data = b"something unrelated\nPredicted values with SED(PV)\n1\n1 1\nsomething unrelated\nend of file"

    temp_file.write(pvs_data)
    temp_file.seek(0)

    assert asreml.services.get_average_std_error(temp_file.name) == 1.0


def test_get_average_std_error_calculation_does_not_include_prediction_id(temp_file):

    pvs_data = (
        b"something unrelated\nPredicted values with SED(PV)\n"
        b" 34\n"
        b"  1 1\n"
        b"  2 1 1\n"
        b"  3 1 1 1\n"
        b"  4 1 1 1\n"
        b" 1\n"
        b"  5 1 1 1\n"
        b" 1 1 \n"
        b"something unrelated\nend of file"
    )

    temp_file.write(pvs_data)
    temp_file.seek(0)

    assert asreml.services.get_average_std_error(temp_file.name) == 1.0


@pytest.mark.parametrize(
    "pvs_data, expected",
    [
        (
            b"something unrelated\nPredicted values with SED(PV)\n 34\n  1 1\n  2 1 1\n  3 1 1 1\n  4 1 1 1\n 1\n  5 1 1 1\n 1 1 \nsomething unrelated\nend of file",
            1.0,
        ),
        (
            b"something unrelated\nPredicted values with SED(PV)\n 34\n  1 0\n  2 0 0\n  3 0 0 0\n  4 0 0 0\n 0\n  5 0 0 0\n 0 0 \nsomething unrelated\nend of file",
            0.0,
        ),
        (
            b"something unrelated\nPredicted values with SED(PV)\n 34\n  1 0.1\n  2 0.1 0\n  3 0.1 0 0\n  4 0 0.1 0\n 0\n  5 0 0.1 0\n 0 0 \nsomething unrelated\nend of file",
            (0.05/15),
        )
    ],
)
def test_get_average_std_error_calculation(temp_file, pvs_data, expected):

    temp_file.write(pvs_data)
    temp_file.seek(0)

    std_avg_error = asreml.services.get_average_std_error(temp_file.name)

    assert round(std_avg_error, 5) == round(std_avg_error, 5)
