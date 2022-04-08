from uuid import uuid4
from af.pipeline.analysis_request import AnalysisRequest
from af.pipeline.asreml.analyze import AsremlAnalyze
from af.pipeline.db.core import DBConfig


def test_result_file_name(mocker, analysis_request):
    # setup db mocks
    mocker.patch.object(DBConfig, "get_session")
    mocker.patch("af.pipeline.db.services.get_analysis_by_request_id")
    reqId = str(uuid4())
    analysis_request.requestId = reqId

    asreml_analyze: AsremlAnalyze = AsremlAnalyze(analysis_request=analysis_request)

    assert asreml_analyze.report_file_path == f"{analysis_request.outputFolder}{reqId}_report.xlsx"
