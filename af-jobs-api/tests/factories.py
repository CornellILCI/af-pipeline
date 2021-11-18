import uuid
from datetime import datetime

import factory
from af_request import api_models, models
from database import Property, db
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

    creator_id = factory.Faker("pystr", min_chars=7, max_chars=7)
    creation_timestamp = factory.Faker("date_time_this_year", tzinfo=UTC)
    modifier_id = factory.Faker("pystr", min_chars=7, max_chars=7)
    modification_timestamp = factory.Faker("date_time_this_year", tzinfo=UTC)


class RequestFactory(CreationModificationBaseFactory):

    uuid = factory.Faker("uuid4")
    type = "ANALYZE"
    institute = factory.Faker("pystr", min_chars=7, max_chars=7)
    crop = factory.Faker("pystr", min_chars=5, max_chars=5)
    status = factory.Faker("word", ext_word_list=["PENDING", "IN-PROGRESS", "DONE", "FAILURE"])
    requestor_id = factory.Faker("pystr", min_chars=7, max_chars=7)
    is_void = False
    engine = factory.Faker("pystr", min_chars=7, max_chars=7)
    msg = factory.Faker("text")

    class Meta:
        model = models.Request


class PropertyFactory(CreationModificationBaseFactory):

    id = factory.Faker("pyint", min_value=1)
    code = factory.Faker("pystr", min_chars=5, max_chars=5)
    name = factory.Faker("pystr", min_chars=5, max_chars=5)
    label = factory.Faker("text", max_nb_chars=10)
    description = factory.Faker("text", max_nb_chars=16)
    type = factory.Faker("pystr", min_chars=10, max_chars=10)
    data_type = factory.Faker("pystr", min_chars=5, max_chars=5)
    statement = factory.Faker("text", max_nb_chars=10)
    is_void = False

    class Meta:
        model = Property


class JobFactory(Factory):

    id = factory.Faker("pyint", min_value=1)
    name = factory.Faker("pystr", min_chars=5, max_chars=5)
    time_start = factory.Faker("pystr", min_chars=5, max_chars=5)
    time_end = factory.Faker("pystr", min_chars=5, max_chars=5)
    output_path = factory.Faker("pystr", min_chars=5, max_chars=5)
    analysis_id = factory.Faker("pyint", min_value=1)

    status = factory.Faker("word", ext_word_list=["PENDING", "IN-PROGRESS", "DONE", "FAILURE"])
    status_message = factory.Faker("text")

    class Meta:
        model = models.Job


class AnalysisFactory(CreationModificationBaseFactory):

    id = factory.Faker("pyint", min_value=1)
    name = factory.Faker("pystr", min_chars=5, max_chars=5)
    description = factory.Faker("text", max_nb_chars=16)
    request_id = factory.Faker("pyint", min_value=1)
    status = factory.Faker("word", ext_word_list=["PENDING", "IN-PROGRESS", "DONE", "FAILURE"])

    prediction_id = factory.Faker("pyint", min_value=1)
    model_id = factory.Faker("pyint", min_value=1)
    formula_id = factory.Faker("pyint", min_value=1)
    residual_id = factory.Faker("pyint", min_value=1)
    trait_analysis_pattern_id = factory.Faker("pyint", min_value=1)
    exp_loc_pattern_id = factory.Faker("pyint", min_value=1)
    analysis_objective_id = factory.Faker("pyint", min_value=1)

    analysis_request_data = {
        "experiments": [{
            "experimentId": "10",
            "experimentName": "expt1",
            "occurrences": [{"occurrenceId": "10", "occurrenceName": "occur1"}]
        }],
        "traits": [{"traitId": "1", "traitName": "trait1"}, {"traitId": "2", "traitName": "trait2"}]
    }
    additional_info = factory.Faker("pydict", nb_elements=2, value_types=[str])

    request = factory.SubFactory(RequestFactory, uuid=factory.SelfAttribute("..request_id"))

    @factory.post_generation
    def jobs(obj, create, extracted, **kwargs):
        obj.jobs.append(JobFactory(analysis_id=obj.id))
        obj.jobs.append(JobFactory(analysis_id=obj.id))

    # map for all relationships to Property
    prediction = factory.SubFactory(PropertyFactory, id=factory.SelfAttribute("..prediction_id"))
    model = factory.SubFactory(PropertyFactory, id=factory.SelfAttribute("..model_id"))
    formula = factory.SubFactory(PropertyFactory, id=factory.SelfAttribute("..formula_id"))
    residual = factory.SubFactory(PropertyFactory, id=factory.SelfAttribute("..residual_id"))
    trait_analysis_pattern = factory.SubFactory(
        PropertyFactory, id=factory.SelfAttribute("..trait_analysis_pattern_id")
    )
    exp_loc_pattern = factory.SubFactory(PropertyFactory, id=factory.SelfAttribute("..exp_loc_pattern_id"))
    analysis_objective = factory.SubFactory(PropertyFactory, id=factory.SelfAttribute("..analysis_objective_id"))

    class Meta:
        model = models.Analysis


class AnalysisRequestParametersFacotry(Factory):

    dataSource = factory.Faker("word", ext_word_list=["EBS", "BRAPI"])
    dataSourceUrl = factory.Faker("pystr_format", string_format="http://test/{{random_int}}")
    dataSourceAccessToken = factory.Faker("pystr", min_chars=32, max_chars=32)
    crop = factory.Faker("pystr", min_chars=5, max_chars=5)
    requestorId = factory.Faker("pystr", min_chars=7, max_chars=7)
    institute = factory.Faker("pystr", min_chars=7, max_chars=7)
    analysisType = "ANALYZE"
    experiments = [{
        "experimentId": "10",
        "experimentName": "expt1",
        "occurrences": [{"occurrenceId": "10", "occurrenceName": "occur1"}]
    }]
    traits = [{"traitId": "1", "traitName": "trait1"}, {"traitId": "2", "traitName": "trait2"}]
    analysisObjectivePropertyId = factory.Faker("pystr", min_chars=10, max_chars=10)
    analysisConfigPropertyId = factory.Faker("pystr", min_chars=10, max_chars=10)
    expLocAnalysisPatternPropertyId = factory.Faker("pystr", min_chars=10, max_chars=10)
    configFormulaPropertyId = factory.Faker("pystr", min_chars=10, max_chars=10)
    configResidualPropertyId = factory.Faker("pystr", min_chars=10, max_chars=10)

    class Meta:
        model = api_models.AnalysisRequestParameters
