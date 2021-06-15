import sys, os, json
import argparse
import pandas as pd
from glob import glob
import numpy as np

from orchestrator import config
from orchestrator.app import LOGGER, app
from orchestrator.base import StatusReportingTask
from orchestrator.exceptions import MissingTaskParameter
from pipeline import dpo
from pipeline.data_reader import DataReaderFactory, PhenotypeData
from pipeline.data_reader.exceptions import DataSourceNotAvailableError, DataTypeNotAvailableError
from pipeline.data_reader.models import Experiment, Occurrence, Trait
from pipeline.data_reader.models.enums import DataSource, DataType

# importing dpo script

"""
task calling dpo, celery supplying params
config is broken up into 3 db tables
request needs to be worked out w Sam
datasource is supplied
dpo is an instance of ProcessData class
should load the request and the
"""


@app.task(name="run_dpo", base=StatusReportingTask)
def run_dpo(params):
    # model id = 143

    print(params)

    # config = params.get("config")
    #
    # # figure this out w sam
    # request = params.get("request")
    # source = params.get("dataSource")
    # if not source:
    #     raise MissingTaskParameter("dataSource")
    #
    #
    # api_token = params.get("apiBearerToken")
    # if not api_token:
    #     raise MissingTaskParameter("apiBearerToken")
    #
    # datasource = _get_datasource(source)
    #
    # dpo = ProcessData()
    #
    # id = "67ac5d6f-5cdc-45fd-a2fa-2bc17a2c58bg_SA_0000"
    #
    # with open(f"/home/vince/dev/work/rando/templates/{id}/{id}.req") as req_f:
    #     req = json.load(req_f)
    #
    # with open("/home/vince/dev/work/rando/config/config_00001.cfg") as config_f:
    #     config = json.load(config_f)
    #
    # dpo = ProcessData("EBS", api_base_url=api_url, api_token=api_token)
    #
    # job_input_files = dpo.run(req, config, "/home/vince/dev/work/rando/out")
