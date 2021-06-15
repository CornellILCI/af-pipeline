"""
asremlutil.py
----------------------

Contains utility funcs for accessing asreml related run args
"""

import os

import docker


def get_docker_url():
    return "unix://var/run/docker.sock"


def get_host_inputs_dir():
    return os.getenv("ASREML_INPUTS_DIR")


def get_host_license_dir():
    return os.getenv("ASREML_LICENSE_DIR")


def get_host_outputs_dir():
    return os.getenv("ASREML_OUTPUTS_DIR")


def get_container_license_dir():
    return "/home/asreml/licenses"


def get_container_inputs_dir():
    return "/home/asreml/inputs"


def get_container_outputs_dir():
    return "/home/asreml/outputs"


def get_asreml_command(input_job_file_name, input_data_file_name):
    inputs_dir = get_container_inputs_dir()
    return f'/bin/bash -c "asreml {inputs_dir}/{input_job_file_name} {inputs_dir}/{input_data_file_name}"'


def run_asreml(input_job_file_name, input_data_file_name):
    """
    run_asreml:

    Returns:
        raw_ouput:str

    Raises:

    """

    client = docker.DockerClient(base_url=get_docker_url())
    return client.containers.run(
        "ebsproject/ba-asreml:21.05",
        command=get_asreml_command(input_job_file_name, input_data_file_name),
        volumes={
            get_host_license_dir(): {"bind": get_container_license_dir(), "mode": "rw"},
            get_host_inputs_dir(): {"bind": get_container_inputs_dir(), "mode": "rw"},
            get_host_outputs_dir(): {"bind": get_container_outputs_dir(), "mode": "rw"},
        },
        stderr=True,
    )


def write_input_file(filename: str, content):
    input_dir = get_container_inputs_dir()
    output_file = f"{input_dir}/{filename}"
    with open(output_file, "w") as f:
        f.write(content)
