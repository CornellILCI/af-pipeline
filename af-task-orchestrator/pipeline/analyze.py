#!/usr/bin/env python3

import argparse
import json
import os
import sys
from collections import OrderedDict
from os import path
import re
import subprocess
import hashlib

from datetime import datetime

if os.getenv("PIPELINE_EXECUTOR") is not None and os.getenv("PIPELINE_EXECUTOR") == "SLURM":
    file_dir = path.dirname(os.path.realpath(__file__))
    pipeline_dir = path.dirname(file_dir)
    sys.path.append(pipeline_dir)

from pipeline import dpo
from pipeline.db.core import SessionLocal
from pipeline.db.models import Analysis, Job
from pipeline.db import services as db_services
from pipeline.data_reader.exceptions import DataReaderException
from pipeline.exceptions import DpoException
from pipeline.exceptions import InvalidAnalysisConfig
from pipeline.exceptions import InvalidAnalysisRequest, InvalidExptLocAnalysisPattern
from pipeline import utils


def run(data_source: str, api_url: str, api_token: str, analysis_request, analysis_config, output_folder):
    """Runs the phenotypic analysis for given request.

    Pre process requested data using dpo module and run analysis engine with the job file and data file.
    Save the status of the analysis to the database.

    Args:
        data_source: Type of API data source. EBS/Brapi.
        api_url: Base url for EBS or BRAPI APIs.
        api_token: Access token to extract data.
        analysis_request: Analysis request with data ids and paramters to perform analysis.
        analysis_config: Anaisis model configurations.
        output_folder: Folder to which the output needs to be saved.
    Returns:
        exit code 0 if sucessful. -1 if fialed
    """

    request_id = analysis_request["metadata"]["id"]

    db_session = SessionLocal()

    # Add new analysis
    analysis = Analysis(
        request_id=request_id,
        request_type=utils.get_request_type(analysis_request),
        time_submitted=datetime.utcnow(),
        sha=utils.get_request_sha(analysis_request),
        status="queued"
    )

    analysis = db_services.add(db_session, analysis)

    _dpo = dpo.ProcessData(data_source, api_url, api_token)

    # Run data pre-processing to get asreml job file and processed data files.
    try:
        job_input_files = _dpo.run(analysis_request, analysis_config, output_folder)
    except (DataReaderException, DpoException) as e:
        analysis.status = "failed"
        db_session.commit()
        return str(e)

    for job_input_file in job_input_files:

        job_name = job_input_file["job_name"]
        asreml_job_file = job_input_file["asreml_job_file"]
        data_file = job_input_file["data_file"]

        analysis_engine = utils.get_analysis_engine(analysis_request)

        job = Job(
            analysis_id=analysis.id,
            name=job_name,
            time_start=datetime.utcnow(),
            parent_id=0
        )

        job = db_services.add(db_session, job)

        cmd = [analysis_engine, asreml_job_file, data_file]

        run_result = subprocess.run(cmd, capture_output=True)

        job.status = utils.get_job_status(run_result.stdout, run_result.stderr)

        if job.status > 100:
            job.err_msg = run_result.stderr.decode('utf-8')
        job.time_end = datetime.utcnow()

        print(run_result.stdout.decode('utf-8'))

        db_session.commit()

    analysis.status = "completed"
    db_session.commit()
    return 0


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

    sys.exit(
        run(args.datasource_type, args.api_url, args.api_token, analysis_request, analysis_config, args.output_folder)
    )
