from datetime import datetime

import factory
from af.pipeline import db
from factory import Factory, LazyAttribute, Sequence, post_generation
from factory.alchemy import SQLAlchemyModelFactory
from factory.fuzzy import FuzzyChoice, FuzzyDateTime, FuzzyInteger, FuzzyText
from pytz import UTC
from sqlalchemy import orm


class BaseFactory(SQLAlchemyModelFactory):
    """Base Factory"""

    class Meta:

        abstract = True


class CreationModificationBaseFactory(BaseFactory):
    """Timestamp Base Factory."""

    creator_id = factory.Faker("pystr", min_chars=7, max_chars=7)
    creation_timestamp = factory.Faker("date_time_this_year", tzinfo=UTC)
    modifier_id = factory.Faker("pystr", min_chars=7, max_chars=7)
    modification_timestamp = factory.Faker("date_time_this_year", tzinfo=UTC)
    tenant_id = 1


class JobFactory(CreationModificationBaseFactory):

    id = factory.Sequence(lambda n: n)

    class Meta:
        model = db.models.Job


class VarianceFactory(CreationModificationBaseFactory):

    id = factory.Sequence(lambda n: n)

    job_id = factory.LazyAttribute(lambda obj: obj.job.id)

    job = factory.SubFactory(JobFactory)

    class Meta:
        model = db.models.Variance
