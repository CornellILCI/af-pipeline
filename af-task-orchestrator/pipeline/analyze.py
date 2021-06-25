#!/usr/bin/env python3

import argparse
import hashlib
import json
import os
import re
import subprocess
import sys
from collections import OrderedDict
from datetime import datetime
from os import path

if os.getenv("PIPELINE_EXECUTOR") is not None and os.getenv("PIPELINE_EXECUTOR") == "SLURM":
    file_dir = path.dirname(os.path.realpath(__file__))
    pipeline_dir = path.dirname(file_dir)
    sys.path.append(pipeline_dir)

from pipeline import config
from pipeline import dpo, utils
from pipeline.data_reader.exceptions import DataReaderException
from pipeline.db import services as db_services
from pipeline.db.core import SessionLocal
from pipeline.db.models import Analysis, Job
from pipeline.db import services as db_services
from pipeline.data_reader.exceptions import DataReaderException
from pipeline.exceptions import DpoException
from pipeline.exceptions import AnalysisError, InvalidAnalysisRequest
from pipeline import utils

from pipeline.analysis_request import AnalysisRequest


def run(analysis_request: AnalysisRequest):
    """Runs the phenotypic analysis for given request.

    Pre process requested data using dpo module and run analysis engine with the job file and data file.
    Save the status of the analysis to the database.

    Args:
        analysis_request: Object with all required paramters to run analysis.
    Returns:
        exit code 0 if sucessful. -1 if fialed
    """

    request_id = analysis_request.requestId

    db_session = SessionLocal()

    # Request source
    _request = db_services.get_request(db_session, analysis_request.requestId)

    # Add new analysis
    analysis = Analysis(
        request_id=_request.id,
        name=analysis_request.requestId,
        creation_timestamp=datetime.utcnow(),
        status="IN-PROGRESS",  # TODO: Find, What this status and how they are defined
    )

    analysis = db_services.add(db_session, analysis)

    # Run data pre-processing to get asreml job file and processed data files.
    job_name = f"{analysis_request.requestId}-dpo"
    job_start_time = datetime.utcnow()
    job = Job(
        analysis_id=analysis.id,
        name=job_name,
        time_start=job_start_time,
        creation_timestamp=job_start_time,
        status="IN-PROGRESS",  # TODO: Find, What this status and how they are defined
        status_message="Running DPO",
    )
    try:
        job_input_files = dpo.ProcessData(analysis_request).run()
    except (DataReaderException, DpoException) as e:
        analysis.status = "FAILED"
        job.status = "FAILED"
        job.status_message = str(e)
        job.time_end = datetime.utcnow()
        job.modification_timestamp = datetime.utcnow()
        db_session.commit()
        raise AnalysisError(str(e))

    analysis_engine_meta = db_services.get_analysis_config_meta_data(
        db_session, analysis_request.analysisConfigPropertyId, "engine"
    )

    analysis_engine = config.get_analysis_engine_script(analysis_engine_meta.value)

    for job_input_file in job_input_files:

        job_name = job_input_file["job_name"]
        asreml_job_file = job_input_file["asreml_job_file"]
        data_file = job_input_file["data_file"]

        job_start_time = datetime.utcnow()

        job = Job(
            analysis_id=analysis.id,
            name=job_name,
            time_start=job_start_time,
            creation_timestamp=job_start_time,
            status="IN-PROGRESS",  # TODO: Find, What this status and how they are defined
            status_message="Processing the input request",
        )

        job = db_services.add(db_session, job)
        try:
            cmd = [analysis_engine, asreml_job_file, data_file]
            run_result = subprocess.run(cmd, capture_output=True)
        except Exception as e:
            analysis.status = "FAILED"
            job.status = "FAILED"
            job.status_message = str(e)[:50] #TODO: Change job status field to text in database.
            job.time_end = datetime.utcnow()
            job.modification_timestamp = datetime.utcnow()
            db_session.commit()
            raise AnalysisError(str(e))

        job.status = utils.get_job_status(run_result.stdout, run_result.stderr)

        if job.status > 100:
            job.status_message = run_result.stderr.decode("utf-8")[:50]
        job.modification_timestamp = datetime.utcnow()
        job.time_end = datetime.utcnow()

        print(run_result.stdout.decode("utf-8"))

        db_session.commit()

    analysis.status = "COMPLETED"
    analysis.modification_timestamp = datetime.utcnow()
    db_session.commit()
    return 0


if __name__ == "__main__":

    parser = argparse.ArgumentParser(description="Process input data to feed into analytical engine")

    parser.add_argument("--request_file", help="File path for analysis request")

    args = parser.parse_args()

    if path.exists(args.request_file):
        with open(args.request_file) as f:
            try:
                analysis_request: AnalysisRequest = AnalysisRequest(**json.load(f))
            except ValidationError as e:
                raise InvalidAnalysisRequest(str(e))
    else:
        raise InvalidAnalysisRequest(f"Request file {args.request_file} not found")

    sys.exit(run(analysis_request))
