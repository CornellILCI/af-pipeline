import pytest
import rpy2
from af.pipeline import asreml_r, job_data, job_status
from af.pipeline import db
from mock import ANY, call, patch


@pytest.fixture
def importr(mocker):

    importr = mocker.patch("rpy2.robjects.packages.importr", return_value=mocker.Mock())
    return importr


@pytest.fixture
def asreml_r_lib(importr, mocker):

    asreml_r_lib = mocker.Mock()
    asreml_r_lib.asreml = mocker.Mock(return_value=None)
    importr.return_value = asreml_r_lib
    return asreml_r_lib


@pytest.fixture
def asr(r_base):
    # set convergence as true
    asr = r_base.list(converge=r_base.logical(1))
    return asr


@pytest.fixture
def entry_predictions(r_base):

    entry_prediction = r_base.list(
        pvals=rpy2.robjects.DataFrame(
            {
                "entry": rpy2.robjects.FactorVector(["4", "5"]),
                "predicted.value": rpy2.robjects.FloatVector([4, 5]),
                "std.error": rpy2.robjects.FloatVector([4, 5]),
                "status": rpy2.robjects.StrVector(["4", "5"]),
            }
        )
    )
    return entry_predictions


@pytest.fixture
def r_base_lib(asr, entry_predictions, importr, mocker):

    r_base_lib = mocker.Mock()
    r_base_lib.detach = mocker.Mock()
    r_base_lib.readRDS = mocker.Mock(side_effect=[asr, entry_predictions])
    importr.return_value = r_base_lib
    return r_base_lib


def test_run_job_returns_job_data(mocker, asreml_r_analysis_request, importr):

    mocker.patch("af.pipeline.db.services.create_job")
    mocker.patch("af.pipeline.rpy_utils.read_csv")

    returned_job_data = asreml_r.analyze.AsremlRAnalyze(asreml_r_analysis_request).run_job(
        job_data.JobData(
            job_params=job_data.JobParams(formula="test ~ formula", residual="test ~ residual", predictions=[])
        )
    )

    assert issubclass(type(returned_job_data), job_data.JobData)


def test_run_job_creates_job_with_inprogess(asreml_r_analysis_request, analysis, mocker, importr, dbsession):

    asreml_r_analyze = asreml_r.analyze.AsremlRAnalyze(asreml_r_analysis_request)
    mocker.patch("af.pipeline.rpy_utils.read_csv")

    create_job = mocker.patch("af.pipeline.db.services.create_job")

    asreml_r_analyze.run_job(
        job_data.JobData(
            job_name="test_job",
            job_params=job_data.JobParams(formula="test ~ formula", residual="test ~ residual", predictions=[]),
        )
    )

    create_job.assert_called_once_with(
        dbsession, analysis.id, "test_job", job_status.JobStatus.INPROGRESS, "Processing input request", {}
    )


def test_asreml_package_imported(asreml_r_analysis_request, importr, mocker):

    asreml_r_analyze = asreml_r.analyze.AsremlRAnalyze(asreml_r_analysis_request)
    mocker.patch("af.pipeline.db.services.create_job")
    mocker.patch("af.pipeline.rpy_utils.read_csv")

    asreml_r_analyze.run_job(
        job_data.JobData(
            job_name="test_job",
            job_params=job_data.JobParams(formula="test ~ formula", residual="test ~ residual", predictions=[]),
        )
    )

    importr.assert_has_calls([call("base"), call("asreml")])


def test_input_data_is_read(asreml_r_analysis_request, mocker, importr):

    asreml_r_analyze = asreml_r.analyze.AsremlRAnalyze(asreml_r_analysis_request)
    mocker.patch("af.pipeline.db.services.create_job")

    read_data = mocker.patch("af.pipeline.rpy_utils.read_csv")

    job_data_ = job_data.JobData(
        job_name="test_job",
        data_file="test_data_file.txt",
        job_params=job_data.JobParams(formula="test ~ formula", residual="test ~ residual", predictions=[]),
    )

    asreml_r_analyze.run_job(job_data_)

    read_data.assert_called_once_with(file=job_data_.data_file)


def test_asreml_run(
    asreml_r_analysis_request,
    asreml_r_input_data,
    asreml_r_fixed_formula,
    asreml_r_random_formula,
    asreml_r_residual,
    asreml_r_lib,
    mocker,
):

    asreml_r_analyze = asreml_r.analyze.AsremlRAnalyze(asreml_r_analysis_request)

    mocker.patch("af.pipeline.db.services.create_job")
    mocker.patch("af.pipeline.rpy_utils.read_csv", return_value=asreml_r_input_data)

    job_data_ = job_data.JobData(
        job_params=job_data.JobParams(
            fixed=asreml_r_fixed_formula.r_repr(), residual=asreml_r_residual.r_repr(), predictions=[]
        )
    )

    asreml_r_analyze.run_job(job_data_)

    asreml_r_lib.asreml.assert_called_once_with(
        fixed=asreml_r_fixed_formula, residual=asreml_r_residual, data=asreml_r_input_data, na_action=ANY
    )


def test_asreml_raises_inavlid_formula_error(asreml_r_analysis_request, importr, mocker):

    asreml_r_analyze = asreml_r.analyze.AsremlRAnalyze(asreml_r_analysis_request)

    mocker.patch("af.pipeline.db.services.create_job")
    mocker.patch("af.pipeline.rpy_utils.read_csv")

    job_data_ = job_data.JobData(
        job_params=job_data.JobParams(fixed="test formula", residual="test residual", predictions=[])
    )

    with pytest.raises(asreml_r.analyze.InvalidFormulaError):
        asreml_r_analyze.run_job(job_data_)


def test_asreml_is_detached_after_run(asreml_r_analysis_request, r_base_lib, mocker):

    asreml_r_analyze = asreml_r.analyze.AsremlRAnalyze(asreml_r_analysis_request)

    mocker.patch("af.pipeline.db.services.create_job")
    mocker.patch("af.pipeline.rpy_utils.read_csv")

    job_data_ = job_data.JobData(
        job_params=job_data.JobParams(fixed="test ~ formula", residual="test ~ residual", predictions=[])
    )

    asreml_r_analyze.run_job(job_data_)

    r_base_lib.detach.assert_called_once_with("package:asreml", unload=True)


def test_post_processing_reads_asr_file(asreml_r_analysis_request, temp_dir, r_base_lib, mocker):

    asreml_r_analyze = asreml_r.analyze.AsremlRAnalyze(asreml_r_analysis_request)

    mocker.patch("af.pipeline.db.services.get_job_by_name")
    import os

    asr_file = os.path.join(temp_dir.name, asreml_r.analyze.AsremlRAnalyze.asr_rds_file_name)
    job_result = asreml_r.analyze.AsremlRJobResult(asr_rds_file=asr_file, prediction_rds_files=[])

    asreml_r_analyze.process_job_result(job_result, {})

    r_base_lib.readRDS.assert_called_once_with(asr_file)


def test_job_is_failed_if_convergence_false(asreml_r_analysis_request, dbsession, r_base, r_base_lib, importr, mocker):

    # asr with convergence failed
    asr = r_base.list(converge=r_base.logical(0))
    r_base_lib.readRDS.side_effect = None
    r_base_lib.readRDS.return_value = asr
    importr.return_value = r_base_lib

    asreml_r_analyze = asreml_r.analyze.AsremlRAnalyze(asreml_r_analysis_request)

    job = db.models.Job()
    mocker.patch("af.pipeline.db.services.get_job_by_name", return_value=job)

    update_job = mocker.patch("af.pipeline.db.services.update_job")

    asreml_r_analyze.process_job_result(asreml_r.analyze.AsremlRJobResult(), {})

    update_job.assert_called_once_with(dbsession, job, job_status.JobStatus.FAILED, "Failed to converge.")


def test_predictions_are_read_when_converged(asreml_r_analysis_request, r_base_lib, mocker):

    asreml_r_analyze = asreml_r.analyze.AsremlRAnalyze(asreml_r_analysis_request)

    mocker.patch("af.pipeline.db.services.get_job_by_name")

    job_result = asreml_r.analyze.AsremlRJobResult(prediction_rds_files=["prediction_file_path_1"])

    asreml_r_analyze.process_job_result(job_result, {})

    r_base_lib.readRDS.assert_called_with("prediction_file_path_1")


def test_entry_predictions_are_written(asreml_r_analysis_request, r_base_lib, mocker):

    asreml_r_analyze = asreml_r.analyze.AsremlRAnalyze(asreml_r_analysis_request)

    mocker.patch("af.pipeline.db.services.get_job_by_name")

    pass


