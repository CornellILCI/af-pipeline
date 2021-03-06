import re
import xml.sax

TAG_VARIANCE_COMPONENTS = "VarianceComponents"
TAG_VPARAMETER = "VParameter"
TAG_SOURCE = "Source"
TAG_VCSTRUCTURE = "VCStructure"
TAG_GAMMA = "Gamma"
TAG_VCOMPONENT = "VComponent"
TAG_ZRATIO = "ZRatio"
TAG_PCCHANGE = "PCchange"
TAG_CONSTRAINTCODE = "ConstraintCode"

TAG_REML_LOGL = "REML_LogL"
TAG_INFO_CRITERIA = "InformationCriteria"
TAG_AKAIKE = "Akaike"
TAG_CONCLUSION = "Conclusion"
TAG_BAYESIAN = "Bayesian"
TAG_PCOUNT = "ParameterCount"

TAG_PREDICTION_COMPONENTS = "PredictionComponent"
TAG_PREDICT_TABLE = "PredictTable"
TAG_CLASSIFY_SET = "ClassifySet"
CLASSIFYSET_VARIABLE_TAG_REGEX = re.compile("Variable_\d+$")
PREDICTION_IDENTIFIER_TAG_REGEX = re.compile("Identifier(_\d+|)$")
TAG_PROW = "Prow"
TAG_CELL = "Cell"
TAG_IDENTIFIER = "Identifier"
TAG_PRED_VALUE = "PredValue"
TAG_STNDERR = "StndErr"
TAG_EPCODE = "EPcode"

TRANSFORM_VARIANCE_TAG = {
    TAG_SOURCE: "source",
    TAG_VCSTRUCTURE: "model",
    TAG_GAMMA: "gamma",
    TAG_VCOMPONENT: "component",
    TAG_ZRATIO: "component_ratio",
    TAG_PCCHANGE: "last_change_percentage",
    TAG_CONSTRAINTCODE: "code",
}

TRANSFORM_MSTAT_TAG = {
    TAG_AKAIKE: "aic",
    TAG_BAYESIAN: "bic",
    TAG_PCOUNT: "components",
    TAG_CONCLUSION: "conclusion",
    TAG_REML_LOGL: "log_lik",
}

TRANSFORM_PREDICTION_TAG = {
    TAG_PREDICT_TABLE: "prediction",
    TAG_PRED_VALUE: "value",
    TAG_STNDERR: "std_error",
    TAG_EPCODE: "e_code",
}


class ASRemlContentHandler(xml.sax.ContentHandler):
    """ASRreml Result XML file content handler
    >>> import xml.sax
    >>> parser = xml.sax.make_parser()
    >>> parser.setFeature(xml.sax.handler.feature_namespaces, 0)
    >>> handler = ASRemlContentHandler()
    >>> parser.setContentHandler(handler)
    >>> parser.parse("/path/to/result.xml")
    >>> print(handler.variances)   # list of dicts of variance data
    >>> print(handler.model_stat)  # contains dict of model_stat data
    >>> print(handler.prediction)  # contains dict of model_stat data
    """

    def __init__(self, job_id: int):
        self.job_id = job_id
        self.variances = []
        self.REML_LogL = None  # for storing the last REML_LogL
        self.model_stat = {"job_id": job_id, "tenant_id": 1, "creator_id": 1}
        self.current_variance = None
        self.current_key = None
        self.current_content = ""
        self.current_prediction = {}
        self.predictions = []
        self.prow = None
        self.in_prediction_components = False
        self.in_variance_components = False
        self.in_vparameter = False
        self.in_prow = False
        self.in_info_criteria = False
        self.in_a_reml_logl = False
        self.in_conclusion = False
        self.in_prediction_classifyset = False
        self.prediction_variables = []  # list of prediction variables
        self.prediction_identifier_index = -1
        self.num_factors = 0

    def startElement(self, tag, attributes):
        self.current_data = tag
        if tag == TAG_VARIANCE_COMPONENTS:
            self.in_variance_components = True
        elif tag == TAG_VPARAMETER and self.in_variance_components:
            self.in_vparameter = True
            self.current_variance = {
                "job_id": self.job_id,
                "tenant_id": 1,
                "creator_id": 1,
            }  # start a new variance object
        elif tag in TRANSFORM_VARIANCE_TAG:
            self.current_key = TRANSFORM_VARIANCE_TAG.get(tag)
        elif tag == TAG_INFO_CRITERIA:
            self.in_info_criteria = True
        elif tag in TRANSFORM_MSTAT_TAG:
            self.current_key = TRANSFORM_MSTAT_TAG.get(tag)
            if tag == TAG_REML_LOGL:
                self.in_a_reml_logl = True
            elif tag == TAG_CONCLUSION:
                self.in_conclusion = True
        elif tag == TAG_PREDICT_TABLE:
            self.in_prediction_components = True
        elif self.in_prediction_components and tag == TAG_CLASSIFY_SET:
            self.in_prediction_classifyset = True
        elif self.in_prediction_components and PREDICTION_IDENTIFIER_TAG_REGEX.match(tag) is not None:
            self.prediction_identifier_index += 1
        elif tag == TAG_PROW and self.in_prediction_components:
            self.in_prow = True
            self.current_prediction = {
                "job_id": self.job_id,
                "tenant_id": 1,
                "creator_id": 1,
            }  # start a new prediction object
        elif tag in TRANSFORM_PREDICTION_TAG:
            self.current_key = TRANSFORM_PREDICTION_TAG.get(tag)

    def endElement(self, tag):
        if tag == TAG_VARIANCE_COMPONENTS:
            self.in_variance_components = False
        elif tag == TAG_VPARAMETER and self.in_variance_components:
            # get current_varariance and store in variances
            self.variances.append(dict(self.current_variance))
            # reset
            self.in_vparameter = False
            self.current_variance = None
        elif tag in TRANSFORM_VARIANCE_TAG:
            self.current_variance[self.current_key] = str(self.current_content).strip()
        elif tag == TAG_INFO_CRITERIA:
            self.in_info_criteria = False
        elif tag in TRANSFORM_MSTAT_TAG:
            self.model_stat[self.current_key] = str(self.current_content).strip()
            if tag == TAG_REML_LOGL:
                self.in_a_reml_logl = False
            elif tag == TAG_CONCLUSION:
                self.model_stat["is_converged"] = str(self.model_stat[self.current_key]).lower() == "logl converged"
                self.in_conclusion = False
        if tag == TAG_PREDICT_TABLE:
            self.in_prediction_components = False
            self.prediction_variables = []
        elif self.in_prediction_components and tag == TAG_CLASSIFY_SET:
            self.in_prediction_classifyset = False
        elif tag == TAG_PROW and self.in_prediction_components:
            # set the num of factor
            self.current_prediction["num_factors"] = self.prediction_identifier_index + 1
            # get current_varariance and store in variances
            self.predictions.append(dict(self.current_prediction))
            # reset
            self.in_prow = False
            self.current_prediction = None
            self.prediction_identifier_index = -1
        elif self.in_prediction_classifyset and CLASSIFYSET_VARIABLE_TAG_REGEX.match(tag) is not None:
            self.prediction_variables.append(str(self.current_content).strip())
            self.num_factors += 1
        elif self.in_prow and PREDICTION_IDENTIFIER_TAG_REGEX.match(tag) is not None:
            factor_name = self.prediction_variables[self.prediction_identifier_index]
            self.current_prediction[factor_name] = str(self.current_content).strip()
        elif tag in TRANSFORM_PREDICTION_TAG:
            self.current_prediction[self.current_key] = str(self.current_content).strip()

        self.current_content = ""

    def characters(self, content):
        if (
            self.in_vparameter
            or self.in_info_criteria
            or self.in_a_reml_logl
            or self.in_conclusion
            or self.in_prow
            or self.in_prediction_classifyset
        ):

            self.current_content += content
