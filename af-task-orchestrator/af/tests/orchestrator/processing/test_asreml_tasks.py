import io

import pytest
from af.orchestrator.processing.asreml.tasks import parse_asremlr
from af.pipeline.db.models import Variance

# def test_parse_asremlr_as_function(mocker, dbsession, sample_asreml_result_string_1):
#     print(dbsession)
#     mocker.patch("af.pipeline.db.core.DBConfig.get_session", return_value=dbsession)

#     params = {"jobId": "123", "resultFilePath": io.StringIO(sample_asreml_result_string_1)}
#     parse_asremlr(params)
#     assert dbsession.query(Variance).count() == 3
