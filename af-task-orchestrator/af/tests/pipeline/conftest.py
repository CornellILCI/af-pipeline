import json
import os
# hacky importing since we need to declare these before we import Base
# since core.py directly declares the vars
import tempfile

import pandas as pd
import pytest
from af.pipeline.db.models import Property
# fixtures import area
from af.tests import factories as model_factory
from rpy2 import robjects
from rpy2.robjects.packages import importr


def get_test_resource_path(testfile, resource_name):
    """Get resource files in the same directory as test file"""
    currentdir = os.path.dirname(os.path.realpath(testfile))
    return os.path.join(currentdir, resource_name)


def get_json_resource(testfile, json_file_name):
    """Reads json file from given file path."""
    file_path = get_test_resource_path(testfile, json_file_name)
    with open(file_path) as file_:
        json_ = json.load(file_)
    return json_


def get_test_analysis_request():

    from af.pipeline.analysis_request import AnalysisRequest, Experiment, Occurrence, Trait

    # output_folder = tempfile.TemporaryDirectory()
    analysis_request = AnalysisRequest(
        requestId="test_id",
        dataSource="EBS",
        dataSourceUrl="http://test.org",
        dataSourceAccessToken="",
        experiments=[
            Experiment(
                experimentId="1",
                experimentName="name1",
                occurrences=[
                    Occurrence(occurrenceId="1", occurrenceName="occur1", locationId="1", locationName="loc1"),
                    Occurrence(occurrenceId="2", occurrenceName="occur2", locationId="2", locationName="loc2"),
                ],
            )
        ],
        traits=[Trait(traitId="1", traitName="trait1")],
        analysisObjectivePropertyId="1",
        analysisConfigPropertyId="1",
        expLocAnalysisPatternPropertyId="1",
        configFormulaPropertyId="1",
        configResidualPropertyId="1",
        outputFolder="/tmp/",
        configPredictionPropertyIds=["19"],
    )
    return analysis_request


def get_test_plots() -> pd.DataFrame:
    """return a mock plots dataframe"""

    columns = [
        "plot_id",
        "expt_id",
        "loc_id",
        "occurr_id",
        "entry_id",
        "pa_x",
        "pa_y",
        "rep_factor",
        "blk",
        "plot_qc",
    ]
    data = [
        [2909, 4, 6, 7, 180, 3, 5, 1, 1, "G"],
        [2910, 4, 6, 7, 103, 4, 5, 1, 1, "G"],
    ]
    return pd.DataFrame(data, columns=columns)


def get_test_plot_measurements() -> pd.DataFrame:
    """return a mock plot measurement dataframe"""

    columns = ["plot_id", "trait_id", "trait_qc", "trait_value"]
    data = [
        [2909, 1, "G", 6.155850575],
        [2910, 1, "G", 6.751358238],
    ]
    return pd.DataFrame(data, columns=columns)


@pytest.fixture
def result_dir(tmpdir_factory):

    result_dir = tmpdir_factory.mktemp("data")
    return str(result_dir)


@pytest.fixture(scope="class")
def analysis_fields():
    return [
        type(
            "PropertyResult",
            (object,),
            {
                "Property": Property(code="loc", data_type="!A"),
                "property_meta": {"definition": "loc_id", "condition": "!SORTALL !PRUNEALL"},
            },
        ),
        type(
            "PropertyResult",
            (object,),
            {
                "Property": Property(code="expt", data_type="!A"),
                "property_meta": {"definition": "expt_id", "condition": "!LL 32"},
            },
        ),
        type(
            "PropertyResult",
            (object,),
            {"Property": Property(code="entry", data_type="!A"), "property_meta": {"definition": "entry_id"}},
        ),
        type(
            "PropertyResult",
            (object,),
            {"Property": Property(code="plot", data_type="!A"), "property_meta": {"definition": "plot_id"}},
        ),
        type(
            "PropertyResult",
            (object,),
            {"Property": Property(code="col", data_type="!I"), "property_meta": {"definition": "pa_x"}},
        ),
        type(
            "PropertyResult",
            (object,),
            {"Property": Property(code="row", data_type="!I"), "property_meta": {"definition": "pa_y"}},
        ),
        type(
            "PropertyResult",
            (object,),
            {"Property": Property(code="rep", data_type="!A"), "property_meta": {"definition": "rep_factor"}},
        ),
    ]


@pytest.fixture(scope="class")
def analysis_fields_class(request, analysis_fields):
    request.cls.analysis_fields = analysis_fields


@pytest.fixture(scope="class")
def analysis_formula():
    analysis_formula = Property(statement="{trait_name} ~ mu rep !r entry !f mv")
    return analysis_formula


@pytest.fixture(scope="class")
def analysis_r_formula():
    analysis_formula = Property(statement="fixed={trait_name} ~ mu rep, random=entry")
    return analysis_formula


@pytest.fixture(scope="class")
def analysis_formula_class(request, analysis_formula):
    request.cls.analysis_formula = analysis_formula


@pytest.fixture(scope="class")
def analysis_residual():
    return Property(statement="ar1(row).ar1(col)")


@pytest.fixture(scope="class")
def analysis_residual_class(request, analysis_residual):
    request.cls.analysis_residual = analysis_residual


@pytest.fixture(scope="class")
def analysis_prediction():
    return Property(statement="entry !PRESENT entry !SED !TDIFF")


@pytest.fixture(scope="class")
def analysis_prediction_class(request, analysis_prediction):
    request.cls.analysis_prediction = analysis_prediction


@pytest.fixture
def sommer_analysis_request():

    from af.pipeline.data_reader.models.enums import DataSource

    sommer_analysis_request = get_test_analysis_request()
    sommer_analysis_request.requestId = "test-request-id"

    sommer_analysis_request.dataSource = DataSource.BRAPI

    return sommer_analysis_request


@pytest.fixture
def analysis_request():

    analysis_request = get_test_analysis_request()
    return analysis_request


@pytest.fixture
def mesl_analysis_pattern(mocker):
    exp_location_analysis_pattern_stub = Property(code="MESL")
    _mock = mocker.patch("af.pipeline.db.services.get_property", return_value=exp_location_analysis_pattern_stub)
    return _mock


@pytest.fixture
def meml_analysis_pattern(mocker):

    exp_location_analysis_pattern_stub = Property(code="MEML")
    _mock = mocker.patch("af.pipeline.db.services.get_property", return_value=exp_location_analysis_pattern_stub)
    return _mock


@pytest.fixture
def plot_columns():

    return [
        "plot_id",
        "expt_id",
        "loc_id",
        "occurr_id",
        "entry_id",
        "entry_name",
        "entry_type",
        "pa_x",
        "pa_y",
        "rep_factor",
        "blk",
        "plot_qc",
    ]


@pytest.fixture
def plot_measurements_columns():
    return ["plot_id", "trait_id", "trait_qc", "trait_value"]


@pytest.fixture
def me_plots_mock(mocker, plot_columns):

    plots_stub = [
        pd.DataFrame(
            columns=plot_columns,
            data=[
                [2909, 1, 1, 1, 1, "entry_name1", "entry_type", 1, 1, 1, 1, "G"],
                [2910, 1, 1, 1, 2, "entry_name2", "entry_type", 1, 2, 1, 1, "G"],
            ],
        ),
        pd.DataFrame(
            columns=plot_columns,
            data=[
                [2911, 1, 2, 2, 3, "entry_name3", "entry_type", 1, 1, 1, 1, "G"],
                [2912, 1, 2, 2, 4, "entry_name4", "entry_type", 1, 2, 1, 1, "G"],
            ],
        ),
        pd.DataFrame(
            columns=plot_columns,
            data=[
                [2913, 2, 1, 3, 5, "entry_name5", "entry_type", 1, 1, 1, 1, "G"],
                [2914, 2, 1, 3, 6, "entry_name6", "entry_type", 1, 2, 1, 1, "G"],
            ],
        ),
        pd.DataFrame(
            columns=plot_columns,
            data=[
                [2915, 2, 2, 4, 7, "entry_name7", "entry_type", 1, 1, 1, 1, "G"],
                [2916, 2, 2, 4, 8, "entry_name8", "entry_type", 1, 2, 1, 1, "G"],
            ],
        ),
    ]

    plots_mock = mocker.patch(
        "af.pipeline.data_reader.phenotype_data_ebs.PhenotypeDataEbs.get_plots", side_effect=plots_stub
    )

    return plots_mock


@pytest.fixture
def me_plot_measurements_mock(mocker, plot_measurements_columns):

    import pandas as pd

    plot_measurements_stub = [
        pd.DataFrame(
            columns=plot_measurements_columns,
            data=[
                [2909, 1, "G", 6.155850575],
                [2910, 1, "G", 6.751358238],
            ],
        ),
        pd.DataFrame(
            columns=plot_measurements_columns,
            data=[
                [2909, 2, "G", 6.155850575],
                [2910, 2, "G", 6.751358238],
            ],
        ),
        pd.DataFrame(
            columns=plot_measurements_columns,
            data=[
                [2911, 1, "G", 6.155850575],
                [2912, 1, "G", 6.751358238],
            ],
        ),
        pd.DataFrame(
            columns=plot_measurements_columns,
            data=[
                [2911, 2, "G", 6.155850575],
                [2912, 2, "G", 6.751358238],
            ],
        ),
        pd.DataFrame(
            columns=plot_measurements_columns,
            data=[
                [2913, 1, "G", 6.155850575],
                [2914, 1, "G", 6.751358238],
            ],
        ),
        pd.DataFrame(
            columns=plot_measurements_columns,
            data=[
                [2913, 2, "G", 6.155850575],
                [2914, 2, "G", 6.751358238],
            ],
        ),
        pd.DataFrame(
            columns=plot_measurements_columns,
            data=[
                [2915, 1, "G", 6.155850575],
                [2916, 1, "G", 6.751358238],
            ],
        ),
        pd.DataFrame(
            columns=plot_measurements_columns,
            data=[
                [2915, 2, "G", 6.155850575],
                [2916, 2, "G", 6.751358238],
            ],
        ),
    ]
    plot_data_mock = mocker.patch(
        "af.pipeline.data_reader.phenotype_data_ebs.PhenotypeDataEbs.get_plot_measurements",
        side_effect=plot_measurements_stub,
    )
    return plot_data_mock


@pytest.fixture
def me_occurrence_mock(mocker):

    from af.pipeline.data_reader import models as dr_models

    occurrence_mock = mocker.patch(
        "af.pipeline.data_reader.phenotype_data_ebs.PhenotypeDataEbs.get_occurrence",
        side_effect=[
            dr_models.Occurrence(
                occurrence_id=1,
                occurrence_name="occur1",
                experiment_id=1,
                experiment_name="name1",
                location_id=1,
                location="loc1",
            ),
            dr_models.Occurrence(
                occurrence_id=2,
                occurrence_name="occur2",
                experiment_id=1,
                experiment_name="name1",
                location_id=2,
                location="loc2",
            ),
            dr_models.Occurrence(
                occurrence_id=3,
                occurrence_name="occur3",
                experiment_id=2,
                experiment_name="name2",
                location_id=1,
                location="loc1",
            ),
            dr_models.Occurrence(
                occurrence_id=4,
                occurrence_name="occur4",
                experiment_id=2,
                experiment_name="name2",
                location_id=2,
                location="loc2",
            ),
        ],
    )

    return occurrence_mock


@pytest.fixture
def me_trait_mock(mocker):

    from af.pipeline.data_reader import models as dr_models

    trait_mock = mocker.patch(
        "af.pipeline.data_reader.phenotype_data_ebs.PhenotypeDataEbs.get_trait",
        side_effect=[
            dr_models.Trait(trait_id=1, trait_name="trait1", abbreviation="trait_abbrev_1"),
            dr_models.Trait(trait_id=2, trait_name="trait2", abbreviation="trait_abbrev_2"),
        ],
    )

    return trait_mock


@pytest.fixture
def me_analysis_request(analysis_request, result_dir):

    from af.pipeline.analysis_request import Experiment, Occurrence, Trait

    analysis_request.experiments.append(
        Experiment(
            experimentId="2",
            experimentName="name2",
            occurrences=[
                Occurrence(occurrenceId="3", occurrenceName="occur3", locationId="1", locationName="loc1"),
                Occurrence(occurrenceId="4", occurrenceName="occur4", locationId="2", locationName="loc2"),
            ],
        )
    )

    analysis_request.traits.append(Trait(traitId="2", traitName="trait2"))

    analysis_request.outputFolder = result_dir

    return analysis_request


@pytest.fixture
def mesl_analysis_request(
    mocker,
    me_analysis_request,
    me_plots_mock,
    me_plot_measurements_mock,
    me_occurrence_mock,
    me_trait_mock,
    analysis_fields,
    analysis_r_formula,
    analysis_residual,
    analysis_prediction,
):

    mocker.patch("af.pipeline.db.services.get_analysis_config_module_fields", return_value=analysis_fields)

    get_property_stubs = [Property(code="MESL")]
    get_property_stubs.extend([analysis_r_formula, analysis_residual, analysis_prediction] * 4)
    mock_props = mocker.patch("af.pipeline.db.services.get_property", side_effect=get_property_stubs)

    return me_analysis_request


@pytest.fixture
def meml_analysis_request(
    mocker,
    me_analysis_request,
    me_plots_mock,
    me_plot_measurements_mock,
    me_occurrence_mock,
    me_trait_mock,
    analysis_fields,
    analysis_r_formula,
    analysis_residual,
    analysis_prediction,
):

    mocker.patch("af.pipeline.db.services.get_analysis_config_module_fields", return_value=analysis_fields)

    get_property_stubs = [Property(code="MEML")]
    get_property_stubs.extend([analysis_r_formula, analysis_residual, analysis_prediction] * 4)
    mock_props = mocker.patch("af.pipeline.db.services.get_property", side_effect=get_property_stubs)

    return me_analysis_request


@pytest.fixture
def job(dbsession):

    model_factory.JobFactory._meta.sqlalchemy_session = dbsession
    job = model_factory.JobFactory()
    dbsession.commit()
    return job


@pytest.fixture
def jobs(dbsession):

    model_factory.JobFactory._meta.sqlalchemy_session = dbsession
    jobs = model_factory.JobFactory.create_batch(size=2)
    return jobs


@pytest.fixture
def variance(dbsession, job):

    model_factory.VarianceFactory._meta.sqlalchemy_session = dbsession

    variance = model_factory.VarianceFactory(job=job)

    return variance


@pytest.fixture
def variances(dbsession, jobs):

    model_factory.VarianceFactory._meta.sqlalchemy_session = dbsession

    variance_1 = model_factory.VarianceFactory(job=jobs[0], source="source1")
    variance_2 = model_factory.VarianceFactory(job=jobs[1], source="source1")
    variance_3 = model_factory.VarianceFactory(job=jobs[1], source="source2")

    return [variance_1, variance_2, variance_3]


@pytest.fixture
def predictions_df():

    return pd.DataFrame(
        columns=["job_id", "entry", "loc", "value", "std_error", "e_code", "num_factors"],
        data=[
            [1, 1, None, 1, 1.4, "E", 1],
            [1, 2, None, 1, 1.5, "E", 1],
            [1, None, 1, 1, 1.4, "E", 1],
            [1, 1, 1, 1, 1.5, "E", 2],
            [1, 2, 1, 1, 1.5, "E", 2],
        ],
    )


@pytest.fixture
def analysis(mocker, dbsession):

    mocker.patch("af.pipeline.db.core.DBConfig.get_session", return_value=dbsession)

    model_factory.RequestFactory._meta.sqlalchemy_session = dbsession
    model_factory.AnalysisFactory._meta.sqlalchemy_session = dbsession

    analysis = model_factory.AnalysisFactory()

    return analysis


@pytest.fixture
def asreml_r_analysis_request(analysis_request, analysis):
    analysis_request.requestId = analysis.request.uuid
    return analysis_request


@pytest.fixture
@robjects.packages.no_warnings
def r_base():
    r_base = importr("base")
    return r_base


@pytest.fixture
def asreml_r_input_data():
    return robjects.DataFrame({"a": 5})


class RFormulaMock(robjects.Formula):
    def __eq__(self, other):
        return self.r_repr() == other.r_repr()


@pytest.fixture
def asreml_r_fixed_formula():
    return RFormulaMock("test ~ formula")


@pytest.fixture
def asreml_r_random_formula():
    return RFormulaMock("~random")


@pytest.fixture
def asreml_r_residual():
    return RFormulaMock("test ~ residual")
