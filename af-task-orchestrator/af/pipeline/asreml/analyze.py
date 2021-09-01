import os
import subprocess
import sys
from datetime import datetime
from os import path

if os.getenv("PIPELINE_EXECUTOR") is not None and os.getenv("PIPELINE_EXECUTOR") == "SLURM":
    file_dir = path.dirname(os.path.realpath(__file__))
    pipeline_dir = path.dirname(file_dir)
    sys.path.append(pipeline_dir)

from af.pipeline.analyze import Analyze
from af.pipeline import config, utils
from af.pipeline.asreml.dpo import AsremlProcessData
from af.pipeline.analysis_request import AnalysisRequest
from af.pipeline.asreml import services as asreml_services
from af.pipeline.data_reader.exceptions import DataReaderException
from af.pipeline.db import services as db_services
from af.pipeline.db.core import DBConfig
from af.pipeline.db.models import Analysis, Job
from af.pipeline.exceptions import AnalysisError, DpoException


class AsremlAnalyze(Analyze):

    dpo_cls = AsremlProcessData
    engine_script = "asreml"

    def __init__(self, analysis_request: AnalysisRequest, *args, **kwargs):
        """Constructor.

        Constructs analysis db record and other required objects.

        Args:
            analysis_request: Object with all required inputs to run analysis.
        """

        self.analysis_request = analysis_request

        self.db_session = DBConfig.get_session()

        # Request source, DB record
        self._analysis_request = db_services.get_request(self.db_session, analysis_request.requestId)

        # load existing analysis record OR create if it does not exist
        self.analysis = db_services.get_analysis_by_request_and_name(
            self.db_session, request_id=self._analysis_request.id, name=analysis_request.requestId
        )

        if not self.analysis:
            # Create DB record for Analysis
            self.analysis = Analysis(
                request_id=self._analysis_request.id,
                name=analysis_request.requestId,
                creation_timestamp=datetime.utcnow(),
                status="IN-PROGRESS",  # TODO: Find, What this status and how they are defined
            )

            self.analysis = db_services.add(self.db_session, self.analysis)

        self.output_file_path = path.join(analysis_request.outputFolder, "result.zip")
        # the engine script would have been determined from get_analyze_object so just pass it here


    def pre_process(self):
        # Run data pre-processing to get asreml job file and processed data files.
        job_name = f"{self.analysis_request.requestId}-dpo"
        job_status = "IN-PROGRESS"
        status_message = "Running Data Pre-Processing."

        job = self.__get_new_job(job_name, job_status, status_message)

        try:
            job_input_files = self.get_process_data(self.analysis_request).run()
            self.__update_job(job, "IN-PROGRESS", "Data Pre-Processing completed.")
            return job_input_files
        except (DataReaderException, DpoException) as e:
            self.analysis.status = "FAILED"
            self.__update_job(job, "FAILED", "Failed during Data Pre-Processing.")
            raise AnalysisError(str(e))
        finally:
            self.db_session.commit()

    def analyze(self, job_input_files):
        """Takes a list of analysis job objects and run analysis for each.
        example:
            [
                {
                    "job_name": "job1"
                    "data_file": "/test/test.csv",
                    "asreml_job_file": "/test/test.as"
                }
            ]
        Returns:
            List of job output object with below fields,
            [
                {
                    "job_name": "job1",
                    "job_id": "jobId1",
                    "job_result_dir": "/test/"
                }
            ]
        """

        # output of each analysis job
        job_results = []
        engine_script = self.get_engine_script()
        for job_input_file in job_input_files:
            job_result = self.run_job(job_input_file, engine_script)
            job_results.append(job_result)

        self.analysis.status = "COMPLETED"
        self.analysis.modification_timestamp = datetime.utcnow()
        self.db_session.commit()

        return job_results

    def get_engine_script(self):
        return self.engine_script

    def run_job(self, job_input_file, analysis_engine=None):
        if not analysis_engine:
            analysis_engine = self.get_engine_script()

        job_name = job_input_file["job_name"]
        asreml_job_file = job_input_file["asreml_job_file"]
        data_file = job_input_file["data_file"]
        job_dir = utils.get_parent_dir(data_file)

        job_status = "IN-PROGRESS"
        status_message = "Processing the input request"

        job = self.__get_new_job(job_name, job_status, status_message)

        try:
            cmd = [analysis_engine, asreml_job_file, data_file]
            _ = subprocess.run(cmd, capture_output=True)
            job = self.__update_job(job, "COMPLETED", "Completed the job.")

            return {"job_name": job_name, "job_id": job.id, "job_result_dir": job_dir}

        except Exception as e:
            self.analysis.status = "FAILED"
            self.__update_job(job, "FAILED", str(e))
            raise AnalysisError(str(e))
        finally:
            self.db_session.commit()

    def post_process(self, job_results):
        for job_result in job_results:
            job_name = job_result["job_name"]
            self.process_job_result(job_name, job_result)

    def process_job_result(self, job_name, job_result: dict):
        try:
            job = db_services.get_job_by_name(self.db_session, job_name)
            job_result_dir = job_result["job_result_dir"]
            asr_file_path = path.join(job_result_dir, f"{job.name}.asr")

            if not path.exists(asr_file_path):
                raise AnalysisError("Analysis result file not found.")

            # parse yhat result and save to db
            yhat_file_path = path.join(job_result_dir, f"{job.name}_yht.txt")
            asreml_services.process_yhat_result(self.db_session, job_result["job_id"], yhat_file_path)

            # parse predictions, model stats from xml and save to db
            asreml_result_xml_path = path.join(job_result_dir, f"{job.name}.xml")
            asreml_services.process_asreml_result(self.db_session, job_result["job_id"], asreml_result_xml_path)

            # zip the result files to be downloaded by the users
            utils.zip_dir(job_result_dir, self.output_file_path, job.name)

            self.__update_job(job, "SUCCESS", "Asreml analysis completed successfully")

        except Exception as e:
            self.analysis.status = "FAILED"
            self.__update_job(job, "FAILED", str(e))
            raise AnalysisError(str(e))
        finally:
            self.db_session.commit()

    def __get_new_job(self, job_name: str, status: str, status_message: str) -> Job:

        job_start_time = datetime.utcnow()
        job = Job(
            analysis_id=self.analysis.id,
            name=job_name,
            time_start=job_start_time,
            creation_timestamp=job_start_time,
            status=status,
            status_message=status_message,
        )

        job = db_services.add(self.db_session, job)

        return job

    def __update_job(self, job: Job, status: str, status_message: str):

        job.status = status
        job.status_message = status_message
        job.time_end = datetime.utcnow()
        job.modification_timestamp = datetime.utcnow()

        return job

    def run(self):
        """Runs the phenotypic analysis for given request.

        Pre process requested data using dpo module and run analysis engine with the job file and data file.
        Save the status of the analysis to the database.

        Returns:
            exit code 0 if sucessful. -1 if fialed
        """

        analysis_input_files = self.pre_process()

        analysis_results = self.analyze(analysis_input_files)

        self.post_process(analysis_results)

        return 0
