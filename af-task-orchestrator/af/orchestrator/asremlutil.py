"""
asremlutil.py
----------------------

Contains utility funcs for accessing asreml related run args
"""

import os

import af.pipeline.asreml.services as asreml_service
import subprocess


def get_container_license_dir():
    return "/home/asreml/licenses"


def get_container_inputs_dir():
    return "/home/asreml/inputs"


def get_container_outputs_dir():
    return "/home/asreml/outputs"


def get_asreml_command(input_job_file_name, input_data_file_name):
    inputs_dir = get_container_inputs_dir()
    return ["asreml", f"{inputs_dir}/{input_job_file_name}", f"{inputs_dir}/{input_data_file_name}"]


def run_asreml(input_job_file_name, input_data_file_name):
    """
    run_asreml:

    Returns:
        raw_ouput:str

    Raises:

    """
    command = get_asreml_command(input_job_file_name, input_data_file_name)
    return subprocess.check_output(command, shell=False)


def write_input_file(filename: str, content):
    input_dir = get_container_inputs_dir()
    output_file = f"{input_dir}/{filename}"
    with open(output_file, "w") as f:
        f.write(content)


def parse_asremlr(job_id: int, filename: str):
    asreml_service.process_asreml_result(None, job_id, filename)
