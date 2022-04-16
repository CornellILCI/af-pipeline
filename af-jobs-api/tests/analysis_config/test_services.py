import pytest
from database import Property


def test_get_analysis_configs(session, analysis_configs):

    from analysis_config import service

    analysis_configs_returned, total_count = service.get_analysis_configs()

    assert total_count > 0


def test_get_analysis_configs_total_count_valid(session, analysis_configs):

    from analysis_config import service

    analysis_configs_returned, total_count = service.get_analysis_configs()

    assert total_count == len(analysis_configs_returned)


def test_get_analysis_configs_has_correct_size(session, analysis_configs):

    from analysis_config import service

    analysis_configs_returned, total_count = service.get_analysis_configs()

    assert total_count == len(analysis_configs)


def test_get_analysis_configs_has_correct_size_with_random_props(session, analysis_configs, random_properties):

    from analysis_config import service

    analysis_configs_returned, total_count = service.get_analysis_configs()

    assert total_count == len(analysis_configs)


@pytest.mark.parametrize(
    "filter_param, filter_value, expected",
    [
        ("design", "test_design", pytest.lazy_fixture("analysis_configs_with_design_metadata")),
        ("engine", "test_engine", pytest.lazy_fixture("analysis_configs_with_engine_metadata")),
        ("trait_level", "test_trait_level", pytest.lazy_fixture("analysis_configs_with_trait_level_metadata")),
        (
            "analysis_objective",
            "test_objective",
            pytest.lazy_fixture("analysis_configs_with_analysis_objective_metadata"),
        ),
        ("exp_analysis_pattern", "test_exp_pattern", pytest.lazy_fixture("analysis_configs_with_exp_pattern_metadata")),
    ],
)
def test_filter_analysis_config_by_exp_pattern(session, filter_param, filter_value, expected):

    from analysis_config import service

    query_params = {filter_param: filter_value}

    analysis_configs_returned, total_count = service.get_analysis_configs(**query_params)

    assert total_count == len(expected)


def test_filter_analysis_config_by_page_size(session, analysis_configs):

    from analysis_config import service

    analysis_configs_returned, total_count = service.get_analysis_configs(page_size=5)

    assert total_count == 5


def test_filter_analysis_config_by_order_by_property_id(session, analysis_configs_unordered):

    from analysis_config import service

    expected_order = []

    for analysis_config in analysis_configs_unordered:
        expected_order.append(analysis_config.id)

    expected_order.sort()

    analysis_configs_returned, total_count = service.get_analysis_configs()

    returned_order = []
    for analysis_config in analysis_configs_returned:
        returned_order.append(analysis_config.id)

    assert expected_order == returned_order


def test_filter_analysis_configs_by_page(session, analysis_configs_unordered):

    from analysis_config import service

    expected_order = []

    for analysis_config in analysis_configs_unordered:
        expected_order.append(analysis_config.id)

    expected_order.sort()

    analysis_configs_returned, total_count = service.get_analysis_configs(page=1, page_size=5)

    returned_order = []
    for analysis_config in analysis_configs_returned:
        returned_order.append(analysis_config.id)

    assert expected_order[5:10] == returned_order
