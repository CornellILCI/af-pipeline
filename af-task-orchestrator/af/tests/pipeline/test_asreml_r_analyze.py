from af.pipeline import asreml_r, job_data, job_status
from mock import patch
import rpy2


class AsremlMock:
    """ARReml mock"""

    def asreml(self, formula, residual=None, data=None):
        return None


def test_run_job_returns_job_data(mocker, asreml_r_analysis_request):

    mocker.patch("af.pipeline.rpy_utils.read_csv")
    mocker.patch("rpy2.robjects.packages.importr", return_value=AsremlMock())

    returned_job_data = asreml_r.analyze.AsremlRAnalyze(asreml_r_analysis_request).run_job(
        job_data.JobData(job_params=job_data.JobParams(formula="test ~ formula", residual="test ~ residual"))
    )

    assert type(returned_job_data) == job_data.JobData


def test_run_job_creates_job_with_inprogess(asreml_r_analysis_request, analysis, mocker, dbsession):

    asreml_r_analyze = asreml_r.analyze.AsremlRAnalyze(asreml_r_analysis_request)
    mocker.patch("af.pipeline.rpy_utils.read_csv")
    mocker.patch("rpy2.robjects.packages.importr", return_value=AsremlMock())

    create_job = mocker.patch("af.pipeline.db.services.create_job")

    asreml_r_analyze.run_job(
        job_data.JobData(
            job_name="test_job", job_params=job_data.JobParams(formula="test ~ formula", residual="test ~ residual")
        )
    )

    create_job.assert_called_once_with(
        dbsession, analysis.id, "test_job", job_status.JobStatus.INPROGRESS, "Processing input request", {}
    )


def test_asreml_package_imported(asreml_r_analysis_request, mocker):

    asreml_r_analyze = asreml_r.analyze.AsremlRAnalyze(asreml_r_analysis_request)
    mocker.patch("af.pipeline.db.services.create_job")
    mocker.patch("af.pipeline.rpy_utils.read_csv")

    asreml_import = mocker.patch("rpy2.robjects.packages.importr", return_value=AsremlMock())

    asreml_r_analyze.run_job(
        job_data.JobData(
            job_name="test_job", job_params=job_data.JobParams(formula="test ~ formula", residual="test ~ residual")
        )
    )

    asreml_import.assert_called_once_with("asreml")


def test_input_data_is_read(asreml_r_analysis_request, mocker):

    asreml_r_analyze = asreml_r.analyze.AsremlRAnalyze(asreml_r_analysis_request)
    mocker.patch("af.pipeline.db.services.create_job")
    mocker.patch("rpy2.robjects.packages.importr", return_value=AsremlMock())

    read_data = mocker.patch("af.pipeline.rpy_utils.read_csv")

    job_data_ = job_data.JobData(
        job_name="test_job",
        data_file="test_data_file.txt",
        job_params=job_data.JobParams(formula="test ~ formula", residual="test ~ residual"),
    )

    asreml_r_analyze.run_job(job_data_)

    read_data.assert_called_once_with(file=job_data_.data_file)


def test_asreml_run(asreml_r_analysis_request, asreml_r_input_data, asreml_r_formula, asreml_r_residual, mocker):

    asreml_r_analyze = asreml_r.analyze.AsremlRAnalyze(asreml_r_analysis_request)

    mocker.patch("af.pipeline.db.services.create_job")
    mocker.patch("rpy2.robjects.packages.importr", return_value=AsremlMock())
    mocker.patch("af.pipeline.rpy_utils.read_csv", return_value=asreml_r_input_data)

    asreml_run = mocker.patch.object(AsremlMock, "asreml")

    job_data_ = job_data.JobData(
        job_params=job_data.JobParams(formula=asreml_r_formula.r_repr(), residual=asreml_r_residual.r_repr())
    )

    asreml_r_analyze.run_job(job_data_)

    asreml_run.assert_called_once_with(
        asreml_r_formula,
        residual=asreml_r_residual,
        data=asreml_r_input_data,
    )


def test_asreml_is_detached_after_run(asreml_r_analysis_request, mocker):

    asreml_r_analyze = asreml_r.analyze.AsremlRAnalyze(asreml_r_analysis_request)
    pass
