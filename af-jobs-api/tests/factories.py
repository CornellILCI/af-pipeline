import uuid
from datetime import datetime

from af_request import api_models, models
from database import db
from factory import Factory, LazyAttribute, Sequence, post_generation
from factory.alchemy import SQLAlchemyModelFactory
from factory.fuzzy import FuzzyChoice, FuzzyDateTime, FuzzyInteger, FuzzyText
from pytz import UTC


class BaseFactory(SQLAlchemyModelFactory):
    """Base Factory"""

    class Meta:

        abstract = True


class CreationModificationBaseFactory(BaseFactory):
    """Timestamp Base Factory."""

    creator_id = FuzzyText(length=7)
    creation_timestamp = FuzzyDateTime(datetime(2021, 1, 1, tzinfo=UTC))
    modifier_id = FuzzyText(length=7)
    modification_timestamp = FuzzyDateTime(datetime(2021, 1, 1, tzinfo=UTC))


class RequestFactory(CreationModificationBaseFactory):

    uuid = LazyAttribute(lambda _: str(uuid.uuid4()))
    type = "ANALYZE"
    institute = FuzzyText(length=10)
    crop = FuzzyText(length=5)
    status = FuzzyChoice(["PENDING", "IN_PROGRESS", "DONE", "FAILURE"])
    requestor_id = FuzzyText(length=10)
    is_void = False
    engine = FuzzyText(length=5)
    msg = FuzzyText(length=20)

    class Meta:
        model = models.Request


class AnalysisRequestParametersFacotry(Factory):

    dataSource = FuzzyChoice(["EBS", "BRAPI"])
    dataSourceUrl = Sequence(lambda n: "http://test/{0}".format(n))
    dataSourceAccessToken = LazyAttribute(lambda _: str(uuid.uuid4()))
    crop = FuzzyText(length=5)
    requestorId = FuzzyText(length=10)
    institute = FuzzyText(length=10)
    analysisType = "ANALYZE"
    experimentIds = ["10"]
    occurrenceIds = ["10"]
    traitIds = ["1", "2"]
    analysisObjectivePropertyId = FuzzyText(length=10)
    analysisConfigPropertyId = FuzzyText(length=10)
    expLocAnalysisPatternPropertyId = FuzzyText(length=10)
    configFormulaPropertyId = FuzzyText(length=10)
    configResidualPropertyId = FuzzyText(length=10)

    class Meta:
        model = api_models.AnalysisRequestParameters
