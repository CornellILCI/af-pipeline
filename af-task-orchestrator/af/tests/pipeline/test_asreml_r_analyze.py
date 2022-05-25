import pytest
import rpy2
from af.pipeline import asreml_r, job_data, job_status
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
def r_base(importr, mocker):

    r_base = mocker.Mock()
    r_base.detach = mocker.Mock()
    importr.return_value = r_base
    return r_base

def test_run_job_returns_job_data(mocker, asreml_r_analysis_request, importr):

    mocker.patch("af.pipeline.db.services.create_job")
    mocker.patch("af.pipeline.rpy_utils.read_csv")

    returned_job_data = asreml_r.analyze.AsremlRAnalyze(asreml_r_analysis_request).run_job(
        job_data.JobData(
            job_params=job_data.JobParams(formula="test ~ formula", residual="test ~ residual", predictions=[])
        )
    )

    assert type(returned_job_data) == job_data.JobData


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
    mocker
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


def test_asreml_is_detached_after_run(asreml_r_analysis_request, r_base, mocker):

    asreml_r_analyze = asreml_r.analyze.AsremlRAnalyze(asreml_r_analysis_request)

    mocker.patch("af.pipeline.db.services.create_job")
    mocker.patch("af.pipeline.rpy_utils.read_csv")

    job_data_ = job_data.JobData(
        job_params=job_data.JobParams(fixed="test ~ formula", residual="test ~ residual", predictions=[])
    )

    asreml_r_analyze.run_job(job_data_)

    r_base.detach.assert_called_once_with("package:asreml", unload=True)


def test_post_processing_reads_asr_file(asreml_r_analysis_request, temp_dir, mocker):
    
    import os

    data_file = os.path.join(temp_dir.name, "data_file")
    job_result = job_data.JobData(data_file=data_file)

    pass

