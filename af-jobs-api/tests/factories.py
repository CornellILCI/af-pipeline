import uuid

from pytz import UTC
from datetime import datetime

from factory import Sequence, LazyAttribute, post_generation, Factory
from factory.alchemy import SQLAlchemyModelFactory
from factory.fuzzy import FuzzyText, FuzzyDateTime, FuzzyChoice

from database import db

from af_request import models


class BaseFactory(Factory):
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
    
    #id = 1
    uuid = LazyAttribute(lambda _: str(uuid.uuid4()))
    type = "ANALYZE"
    #institute = FuzzyText(length=10)
    #crop = FuzzyText(length=5)
    #status = FuzzyChoice(["PENDING", "IN_PROGRESS", "DONE", "FAILURE"])
    #is_void = False
    #engine = db.Column(db.String(20))
    #msg = FuzzyText(length=20)
    
    class Meta:
        model = models.Request

