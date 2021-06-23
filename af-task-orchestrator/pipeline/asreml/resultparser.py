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


class ASRemlContentHandler(xml.sax.ContentHandler):
    def __init__(self):
        self.variances = []
        self.REML_LogL = None  # for storing the last REML_LogL
        self.model_stat = {}
        self.current_variance = None
        self.current_key = None
        self.current_content = ""

        self.in_variance_components = False
        self.in_vparameter = False

        self.in_info_criteria = False
        self.in_a_reml_logl = False
        self.in_conclusion = False

    def startElement(self, tag, attributes):
        self.current_data = tag
        if tag == TAG_VARIANCE_COMPONENTS:
            self.in_variance_components = True
        elif tag == TAG_VPARAMETER and self.in_variance_components:
            self.in_vparameter = True
            self.current_variance = {}  # start a new variance object
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
                self.model_stat["converged"] = str(self.model_stat[self.current_key]).lower() == "logl converged"
                self.in_conclusion = False

        self.current_content = ""

    def characters(self, content):
        if self.in_vparameter or self.in_info_criteria or self.in_a_reml_logl or self.in_conclusion:
            self.current_content += content
