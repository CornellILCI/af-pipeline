import uuid
from datetime import datetime

import factory
from af_request import api_models, models
from database import Property, PropertyConfig, PropertyMeta, db
from factory import Factory, LazyAttribute, Sequence, post_generation
from factory.alchemy import SQLAlchemyModelFactory
from factory.fuzzy import FuzzyChoice, FuzzyDateTime, FuzzyInteger, FuzzyText
from flask import current_app
from flask_sqlalchemy import get_state
from pytz import UTC
from sqlalchemy.orm import scoped_session

Session = scoped_session(
    lambda: get_state(current_app).db.session,
    scopefunc=lambda: get_state(current_app).db.session,
)


class BaseFactory(SQLAlchemyModelFactory):
    """Base Factory"""

    class Meta:

        abstract = True
        sqlalchemy_session = Session


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

    id = factory.Sequence(lambda n: n)

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


class PropertyConfigFactory(CreationModificationBaseFactory):

    id = factory.Sequence(lambda n: n)
    config_property_id = factory.LazyAttribute(lambda obj: obj.property_config_property.id)

    property_config_property = factory.SubFactory(PropertyFactory)

    class Meta:
        model = PropertyConfig


class PropertyMetaFactory(CreationModificationBaseFactory):

    id = factory.Sequence(lambda n: n)

    code = factory.Faker("pystr", min_chars=5, max_chars=5)
    value = factory.Faker("pystr", min_chars=5, max_chars=5)

    property_id = factory.LazyAttribute(lambda obj: obj.property.id)

    property = factory.SubFactory(PropertyFactory)

    class Meta:
        model = PropertyMeta


class RandomPropertyFactory(PropertyFactory):
    @factory.post_generation
    def property_configs(obj, create, extracted, **kwargs):
        obj.property_configs.extend(PropertyConfigFactory.create_batch(size=10, property_id=obj.id))

        # add property config for analysis config itself
        obj.property_configs.append(PropertyConfigFactory(property_id=obj.id, property_config_property=obj))


class AnalysisConfigFactory(PropertyFactory):
    @factory.post_generation
    def property_metas(obj, create, extracted, **kwargs):
        obj.property_metas.extend(PropertyMetaFactory.create_batch(size=10, property=obj))


class AnalysisConfigsPropertyConfigFactory(PropertyConfigFactory):

    property_config_property = factory.SubFactory(AnalysisConfigFactory)


class AnalysisConfigsRootFactory(PropertyFactory):

    code = "analysis_config"

    @factory.post_generation
    def property_configs(obj, create, extracted, **kwargs):

        # add analysis config properties
        obj.property_configs.extend(AnalysisConfigsPropertyConfigFactory.create_batch(size=10, property_id=obj.id))

        # add property config for analysis config itself
        obj.property_configs.append(PropertyConfigFactory(property_id=obj.id, property_config_property=obj))


class AnalysisConfigUnorderedFactory(PropertyFactory):

    @factory.post_generation
    def property_metas(obj, create, extracted, **kwargs):
        obj.property_metas.extend(PropertyMetaFactory.create_batch(size=10, property=obj))


class AnalysisConfigsUnordredPropertyConfigFactory(PropertyConfigFactory):

    property_config_property = factory.SubFactory(AnalysisConfigUnorderedFactory)


class AnalysisConfigsRootUnorderedFactory(PropertyFactory):

    code = "analysis_config"

    @factory.post_generation
    def property_configs(obj, create, extracted, **kwargs):

        # add analysis config properties
        obj.property_configs.extend(
            AnalysisConfigsUnordredPropertyConfigFactory.create_batch(size=10, property_id=obj.id)
        )

        # add property config for analysis config itself
        obj.property_configs.append(PropertyConfigFactory(property_id=obj.id, property_config_property=obj))


class AnalysisConfigWithDesignFactory(PropertyFactory):
    @factory.post_generation
    def property_metas(obj, create, extracted, **kwargs):
        obj.property_metas.append(PropertyMetaFactory(code="design", value="test_design", property=obj))


class AnalysisConfigsWithDesignPropertyConfigFactory(PropertyConfigFactory):

    property_config_property = factory.SubFactory(AnalysisConfigWithDesignFactory)


class AnalysisConfigWithEngineFactory(PropertyFactory):
    @factory.post_generation
    def property_metas(obj, create, extracted, **kwargs):
        obj.property_metas.append(PropertyMetaFactory(code="engine", value="test_engine", property=obj))


class AnalysisConfigsWithEnginePropertyConfigFactory(PropertyConfigFactory):

    property_config_property = factory.SubFactory(AnalysisConfigWithEngineFactory)


class AnalysisConfigWithTraitLevelFactory(PropertyFactory):
    @factory.post_generation
    def property_metas(obj, create, extracted, **kwargs):
        obj.property_metas.append(PropertyMetaFactory(code="trait_level", value="test_trait_level", property=obj))


class AnalysisConfigsWithTraitLevelPropertyConfigFactory(PropertyConfigFactory):

    property_config_property = factory.SubFactory(AnalysisConfigWithTraitLevelFactory)


class AnalysisConfigWithAnalysisObjectiveFactory(PropertyFactory):
    @factory.post_generation
    def property_metas(obj, create, extracted, **kwargs):
        obj.property_metas.append(PropertyMetaFactory(code="analysis_objective", value="test_objective", property=obj))


class AnalysisConfigsWithAnalysisObjectivePropertyConfigFactory(PropertyConfigFactory):

    property_config_property = factory.SubFactory(AnalysisConfigWithAnalysisObjectiveFactory)


class AnalysisConfigWithExpPatternFactory(PropertyFactory):
    @factory.post_generation
    def property_metas(obj, create, extracted, **kwargs):
        obj.property_metas.append(
            PropertyMetaFactory(code="exp_analysis_pattern", value="test_exp_pattern", property=obj)
        )


class AnalysisConfigsWithExpPatternPropertyConfigFactory(PropertyConfigFactory):

    property_config_property = factory.SubFactory(AnalysisConfigWithExpPatternFactory)


class JobFactory(Factory):

    id = factory.Sequence(lambda n: n)
    name = factory.Faker("pystr", min_chars=5, max_chars=5)
    time_start = factory.Faker("pystr", min_chars=5, max_chars=5)
    time_end = factory.Faker("pystr", min_chars=5, max_chars=5)
    output_path = factory.Faker("pystr", min_chars=5, max_chars=5)
    analysis_id = factory.Faker("pyint", min_value=1)

    status = factory.Faker("word", ext_word_list=["PENDING", "IN-PROGRESS", "DONE", "FAILURE"])
    status_message = factory.Faker("text")

    job_data = factory.Dict(
        {
            "trait_name": factory.Faker("pystr", min_chars=5, max_chars=5),
            "location_name": factory.Faker("pystr", min_chars=5, max_chars=5),
        }
    )

    class Meta:
        model = models.Job


class AnalysisFactory(CreationModificationBaseFactory):

    id = factory.Faker("pyint", min_value=1)
    name = factory.Faker("pystr", min_chars=5, max_chars=5)
    description = factory.Faker("text", max_nb_chars=16)
    request_id = factory.Faker("pystr", min_chars=5, max_chars=5)
    status = factory.Faker("word", ext_word_list=["PENDING", "IN-PROGRESS", "DONE", "FAILURE"])

    prediction_id = factory.LazyAttribute(lambda obj: obj.prediction.id)
    model_id = factory.LazyAttribute(lambda obj: obj.model.id)
    formula_id = factory.LazyAttribute(lambda obj: obj.formula.id)
    residual_id = factory.LazyAttribute(lambda obj: obj.residual.id)
    trait_analysis_pattern_id = factory.LazyAttribute(lambda obj: obj.trait_analysis_pattern.id)
    exp_loc_pattern_id = factory.LazyAttribute(lambda obj: obj.exp_loc_pattern.id)
    analysis_objective_id = factory.LazyAttribute(lambda obj: obj.analysis_objective.id)

    analysis_request_data = {
        "experiments": [
            {
                "experimentId": "10",
                "experimentName": "expt1",
                "occurrences": [{"occurrenceId": "10", "occurrenceName": "occur1"}],
            }
        ],
        "traits": [{"traitId": "1", "traitName": "trait1"}, {"traitId": "2", "traitName": "trait2"}],
    }
    additional_info = factory.Faker("pydict", nb_elements=2, value_types=[str])

    request = factory.SubFactory(RequestFactory, uuid=factory.SelfAttribute("..request_id"))

    @factory.post_generation
    def jobs(obj, create, extracted, **kwargs):
        obj.jobs.append(JobFactory(analysis_id=obj.id))
        obj.jobs.append(JobFactory(analysis_id=obj.id))

    # map for all relationships to Property
    prediction = factory.SubFactory(PropertyFactory)
    model = factory.SubFactory(PropertyFactory)
    formula = factory.SubFactory(PropertyFactory)
    residual = factory.SubFactory(PropertyFactory)
    trait_analysis_pattern = factory.SubFactory(PropertyFactory)
    exp_loc_pattern = factory.SubFactory(PropertyFactory)
    analysis_objective = factory.SubFactory(PropertyFactory)

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
    experiments = [
        {
            "experimentId": "10",
            "experimentName": "expt1",
            "occurrences": [{"occurrenceId": "10", "occurrenceName": "occur1"}],
        }
    ]
    traits = [{"traitId": "1", "traitName": "trait1"}, {"traitId": "2", "traitName": "trait2"}]
    analysisObjectivePropertyId = factory.Faker("pyint", min_value=1)
    analysisConfigPropertyId = factory.Faker("pyint", min_value=1)
    expLocAnalysisPatternPropertyId = factory.Faker("pyint", min_value=1)
    configFormulaPropertyId = factory.Faker("pyint", min_value=1)
    configResidualPropertyId = factory.Faker("pyint", min_value=1)

    class Meta:
        model = api_models.AnalysisRequestParameters
