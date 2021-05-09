#!/usr/bin/env python3

import argparse
import json
import os
import sys
from collections import OrderedDict
from os import path

import pipeline.config  # noqa: E402
from pandas import DataFrame  # noqa: E402
from pipeline.data_reader import DataReaderFactory, PhenotypeData  # noqa: E402
from pipeline.data_reader.exceptions import MissingTaskParameter  # noqa: E402
from pipeline.data_reader.exceptions import (DataSourceNotAvailableError,
                                             DataTypeNotAvailableError)
from pipeline.data_reader.models import Experiment, Occurrence
from pipeline.data_reader.models.enums import (DataSource,  # noqa: E402
                                               DataType)
from pipeline.exceptions import InvalidAnalysisConfig  # noqa: E402
from pipeline.exceptions import (InvalidAnalysisRequest,
                                 InvalidExptLocAnalysisPattern)
from pipeline.pandasutil import df_keep_columns  # noqa: E402

from pipeline.data_reader.models import Trait  # noqa: E402; noqa: E402

"""
To manage module imports when run in slurm or imported into celery task,
pipeline python scripts should append parent directory to sys path,
so pipeline as a module can be imported by both celery task and slurm script.
"""
currentdir = path.dirname(os.path.realpath(__file__))
parentdir = path.dirname(currentdir)
sys.path.append(parentdir)


def _get_analysis_request_data_ids(analysis_request):
    try:
        occurrence_ids = analysis_request["data"]["occurrence_id"]
        trait_ids = analysis_request["data"]["trait_id"]
        experiment_ids = analysis_request["data"]["experiment_id"]
    except KeyError as _key_e:
        raise InvalidAnalysisRequest(f"expected data field {_key_e} not found")

    return occurrence_ids, trait_ids, experiment_ids


def _get_analysis_fields(analysis_config):
    try:
        analysis_fields = analysis_config["Analysis_Module"]["fields"]
    except KeyError as _key_e:
        raise InvalidAnalysisConfig(f"'fields' not found")

    return analysis_fields


def _get_input_fields_to_config_fields(analysis_config):
    """A map to rename column names to names defined in analysis config"""

    input_fields_to_config_fields = OrderedDict({"occurr_id": "occid"})
    analysis_fields = _get_analysis_fields(analysis_config)

    for field in analysis_fields:
        try:
            input_field_name = field["definition"]
            config_field_name = field["stat_factor"]
        except KeyError as _key_e:
            raise InvalidAnalysisConfig(f"field {_key_e} not found")

        input_fields_to_config_fields[input_field_name] = config_field_name
    return input_fields_to_config_fields


def _get_traits(data_reader, trait_ids: list[str]) -> list[Trait]:
    traits = []
    for trait_id in trait_ids:
        trait: Trait = data_reader.get_trait(trait_id)
        traits.append(trait)
    return traits


def _sesl_filter(data_reader, analysis_request, analysis_config):
    """Data is split by traits, where each result have plots and plot_measurements from
    multiple occurrences for the same trait.
    """

    plots_by_occurrence_id = {}

    occurrence_ids, trait_ids, experiment_ids = _get_analysis_request_data_ids(analysis_request)

    for occurrence_id in occurrence_ids:
        plots_by_occurrence_id[occurrence_id] = data_reader.get_plots(occurrence_id)

    traits: list[Trait] = _get_traits(trait_ids)

    for trait in traits:

        plots_and_measurements = None

        for occurrence_id in occurrence_ids:

            plots = plots_by_occurrence_id[occurrence_id]
            plot_measurements_ = data_reader.get_plot_measurements(occurrence_id, trait.trait_id)
            if plots_and_measurements is None:
                plots_and_measurements = plots.merge(plot_measurements_, on="plot_id", how="left")
            else:
                plots_and_measurements_ = plots.merge(plot_measurements_, on="plot_id", how="left")
                plots_and_measurements = plots_and_measurements.append(plots_and_measurements_)

        plots_and_measurements = _format_result_data(plots_and_measurements, trait, input_fields_to_config_fields)

        if not plots_and_measurements.empty:
            yield f"{trait.trait_id}", plots_and_measurements, trait


def _seml_filter(data_reader, analysis_request, analysis_config):
    """Data is split by occurrence and trait, where each result have plots and plot_measurements from
    same occurrences and same trait.
    """

    occurrence_ids, trait_ids, experiment_ids = _get_analysis_request_data_ids(analysis_request)
    traits: list[Trait] = _get_traits(trait_ids)

    for occurrence_id in occurrence_ids:
        plots = data_reader.get_plots(occurrence_id)
        for trait in traits:
            plot_measurements_ = data_reader.get_plot_measurements(occurrence_id, trait.trait_id)

            # default is inner join
            plots_and_measurements = plots.merge(plot_measurements_, on="plot_id")

            plots_and_measurements = _format_result_data(plots_and_measurements, trait, input_fields_to_config_fields)

            if not plots_and_measurements.empty:
                yield f"{occurrence_id}_{trait.trait_id}", plots_and_measurements, trait


def _format_result_data(plots_and_measurements, trait, input_fields_to_config_fields):
    # drop trait id
    plots_and_measurements.drop(["trait_id"], axis=1, inplace=True)

    # drop occurrence id
    plots_and_measurements.drop(["occurr_id"], axis=1, inplace=True)

    # For trait value fillna with "NA" string
    plots_and_measurements[["trait_value"]] = plots_and_measurements[["trait_value"]].fillna(value="NA")

    # map trait value column to trait name
    input_fields_to_config_fields["trait_value"] = trait.abbreviation

    # Key only the config field columns
    plots_and_measurements = df_keep_columns(plots_and_measurements, input_fields_to_config_fields.keys())

    plots_and_measurements = plots_and_measurements.rename(columns=input_fields_to_config_fields)

    return plots_and_measurements


def _get_asrml_job_file_lines(job_name, analysis_request, analysis_config, trait: Trait):

    job_file_lines = [job_name]

    request_parameters = analysis_request["parameters"]
    analysis_module = analysis_config["Analysis_Module"]

    # 1: adding the analysis field statements
    analysis_fields = _get_analysis_fields(analysis_config)

    for field in analysis_fields:
        field_line = "\t{stat_factor} {data_type} {condition}".format(
            stat_factor=field["stat_factor"], data_type=field["data_type"], condition=field["condition"]
        )
        job_file_lines.append(field_line)

    # 2: adding trait name
    job_file_lines.append(trait.abbreviation)

    # 3: adding otpions
    data_file_name = f"{job_name}.csv"
    options_line = "{} {}".format(data_file_name, analysis_module["asrmel_options"][0]["options"])
    job_file_lines.append(options_line)

    # 4: adding tabulate
    tabulate_line = "tabulate {}".format(
        analysis_module["tabulate"][0]["statement"].format(trait_name=trait.abbreviation)
    )
    job_file_lines.append(tabulate_line)

    # 5: adding formula
    formula_id = request_parameters["formula"]
    for formula in analysis_module["formula"]:
        if formula["id"] == str(formula_id):
            formula_statement = formula["statement"].format(trait_name=trait.abbreviation)
            job_file_lines.append(formula_statement)
            break

    # 6: adding residual
    residual_id = request_parameters["residual"]
    for residual in analysis_module["residual"]:
        if residual["spatial_id"] == str(residual_id):
            residual_statement = residual["spatial_model"]
            if residual_statement:
                job_file_lines.append(f"residual {residual_statement}")
            break

    # 7: adding prediction
    prediction_id = request_parameters["prediction"][0]
    for prediction in analysis_module["predict"]:
        if prediction["id"] == str(prediction_id):
            prediction_statement = "prediction {}".format(prediction["statement"])
            job_file_lines.append(prediction_statement)
            break

    return job_file_lines


def _write_results(results, output_folder, analysis_request, analysis_config):

    processed_data_files = []
    request_id = analysis_request["metadata"]["id"]
    request_parameters = analysis_request["parameters"]

    for (result_id, result, trait) in results:

        job_name = "{}_{}".format(request_id, result_id)

        job_file_name = f"{job_name}.as"
        data_file_name = f"{job_name}.csv"

        job_file_path = os.path.join(output_folder, job_file_name)
        data_file_path = os.path.join(output_folder, data_file_name)

        result.to_csv(data_file_path, index=False)

        job_file_lines = _get_asrml_job_file_lines(job_name, request_parameters, analysis_config, trait)

        with open(job_file_path, "w") as j_f:
            for line in job_file_lines:
                j_f.write("{}\n".format(line))

        processed_data_files.append({"data_file": data_file_path, "asreml_job_file": job_file_path})

    return processed_data_files


def run(data_source, api_base_url, api_token, analysis_request, analysis_config, output_folder: str):
    """Pre process input data before inputing into analytical engine.

    Extracts plots and plot measurements from api source.
    Prepares the extracted data to feed into analytical engine.

    Args:
        analysis_request: key value object. user submitted analysis request.
        analysis_config: analysis engine configuration to use for given request
        output_folder: directory where processed output files to be saved.

    Returns:
        List of object with following args,
            data_file: File with input data
            asrml_job_file: File with job configuration specific to input request
        example:
            [
                {
                    "data_file": "/test/test.csv",
                    "asrml_job_file": "/test/test.as"
                }
            ]

    Raises:
        InvalidAnalysisConfig, InvalidAnalysisRequest, InvalidExptLocAnalysisPattern
    """

    try:
        data_source: DataSource = DataSource[data_source]
    except KeyError:
        raise DataSourceNotAvailableError(data_source)
    factory = DataReaderFactory(data_source)
    data_reader: PhenotypeData = factory.get_phenotype_data(api_base_url=api_base_url, api_bearer_token=api_token)

    try:
        analysis_parameters = analysis_request["parameters"]
        exptloc_analysis_pattern = analysis_parameters["exptloc_analysis_pattern"]
    except KeyError as _key_e:
        raise InvalidAnalysisRequest(f"field {_key_e} not found")

    if exptloc_analysis_pattern == 1:
        results = _sesl_filter(data_reader, analysis_request, analysis_config)
    elif exptloc_analysis_pattern == 2:
        results = _seml_filter(data_reader, analysis_request, analysis_config)
    else:
        raise InvalidAnalysisExptLocAnalysisPattern(f"Value: {exptloc_analysis_pattern} is invalid")


if __name__ == "__main__":

    parser = argparse.ArgumentParser(description="Process input data to feed into analytical engine")

    parser.add_argument("--request_file", help="File path for analysis request")
    parser.add_argument("--config_file", help="File path for analysis config")
    parser.add_argument("--output_folder", help="Directory to write output files")

    parser.add_argument("--datasource_type", help="Datasource to use EBS or BRAPI")
    parser.add_argument("--api_url", help="Api base url for data source to download input data from")
    parser.add_argument("--api_token", help="Api token to access datasource api")

    args = parser.parse_args()

    if path.exists(args.request_file):
        with open(args.request_file) as f:
            analysis_request = json.load(f)
    else:
        raise InvalidAnalysisRequest(f"Request file {args.request_file} not found")

    if path.exists(args.config_file):
        with open(args.config_file) as f:
            analysis_config = json.load(f)
    else:
        raise InvalidAnalysisConfig(f"Request file {args.config_file} not found")

    if not path.exists(args.output_folder):
        raise ProcessDataException(f"Output folder {args.output_folder} not found")

    sys.exit(run(
        args.datasource_type,
        args.api_url,
        args.api_token,
        analysis_request,
        analysis_config,
        args.output_folder
    ))
