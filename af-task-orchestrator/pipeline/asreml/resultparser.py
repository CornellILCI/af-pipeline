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

TRANSFORM_TAG = {
    TAG_SOURCE: "source",
    TAG_VCSTRUCTURE: "model",
    TAG_GAMMA: "gamma",
    TAG_VCOMPONENT: "component",
    TAG_ZRATIO: "component_ratio",
    TAG_PCCHANGE: "last_change_percentage",
    TAG_CONSTRAINTCODE: "code",
}


class ASRemlContentHandler(xml.sax.ContentHandler):
    def __init__(self):
        self.variances = []
        # self.model_stat = {}
        self.current_variance = None
        self.current_key = None
        self.current_content = ""

        self.in_variance_components = False
        self.in_vparameter = False

    def startElement(self, tag, attributes):
        self.current_data = tag
        if tag == TAG_VARIANCE_COMPONENTS:
            self.in_variance_components = True
        elif tag == TAG_VPARAMETER and self.in_variance_components:
            self.in_vparameter = True
            self.current_variance = {}  # start a new variance object
        elif tag in TRANSFORM_TAG:
            self.current_key = TRANSFORM_TAG.get(tag)

    def endElement(self, tag):
        if tag == TAG_VARIANCE_COMPONENTS:
            self.in_variance_components = False
        elif tag == TAG_VPARAMETER and self.in_variance_components:
            # get current_varariance and store in variances
            self.variances.append(dict(self.current_variance))
            # reset
            self.in_vparameter = False
            self.current_variance = None
        elif tag in (
            TAG_SOURCE,
            TAG_VCSTRUCTURE,
            TAG_GAMMA,
            TAG_VCOMPONENT,
            TAG_ZRATIO,
            TAG_PCCHANGE,
            TAG_CONSTRAINTCODE,
        ):
            self.current_variance[self.current_key] = str(self.current_content).strip()
            self.current_content = ""
        else:
            self.current_content = ""

    def characters(self, content):
        if self.in_vparameter:
            self.current_content += content
