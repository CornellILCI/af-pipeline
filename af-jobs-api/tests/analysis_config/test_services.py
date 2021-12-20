from database import Property


def test_get_analysis_configs(session, analysis_configs):

    from analysis_config import service

    analysis_configs_returned: List[Property] = service.get_analysis_configs()

    assert len(analysis_configs_returned) > 0


def test_get_analysis_configs_has_correct_size(session, analysis_configs):

    from analysis_config import service

    analysis_configs_returned: List[Property] = service.get_analysis_configs()

    assert len(analysis_configs_returned) == len(analysis_configs)


def test_get_analysis_configs_has_correct_size_with_random_props(session, analysis_configs, random_properties):

    from analysis_config import service

    analysis_configs_returned: List[Property] = service.get_analysis_configs()

    assert len(analysis_configs_returned) == len(analysis_configs)


