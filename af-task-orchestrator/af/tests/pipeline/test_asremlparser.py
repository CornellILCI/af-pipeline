import xml.sax

import af.pipeline.asreml.resultparser as parser


def test_simple_test_1(sample_asreml_result_string_1):
    sample_job_id = 123
    handler = parser.ASRemlContentHandler(sample_job_id)
    xml.sax.parseString(sample_asreml_result_string_1, handler)  # NOTE: this is no how we parse files

    num_vars = len(handler.variances)
    print(handler.variances)
    print(handler.model_stat)
    # print(handler.predictions)
    assert num_vars == 3, f"Expecting three variances, got {num_vars}"
    assert handler.variances[0]["job_id"] == sample_job_id
    assert handler.variances[0]["source"] == "entry"
    assert handler.variances[0]["model"] == "IDV_V"
    assert handler.variances[0]["gamma"] == "0.57920334E-07"
    assert handler.variances[0]["component"] == "0.13792020E-06"
    assert handler.variances[0]["component_ratio"] == "0.0000000"
    assert handler.variances[0]["last_change_percentage"] == "0"
    assert handler.variances[0]["code"] == "B"

    # No need ot check [1] and [2]?

    # check the model_stat
    assert handler.model_stat["job_id"] == sample_job_id
    assert handler.model_stat["conclusion"] == "LogL Converged"
    assert handler.model_stat["converged"] == True
    assert handler.model_stat["log_lik"] == "-390.5927"
    assert handler.model_stat["aic"] == "787.1855"
    assert handler.model_stat["bic"] == "799.2775"
    assert handler.model_stat["components"] == "3"

    assert len(handler.predictions) == 180
    assert handler.predictions[0]["e_code"] == "E"
    assert handler.predictions[0]["std_error"] == "0.0846111"
    assert handler.predictions[0]["value"] == "6.6159"
    assert handler.predictions[0]["id"] == "1"
