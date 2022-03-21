from af.pipeline import utils
from af.pipeline.asreml.analyze import AsremlAnalyze  # temporary while we refactor parts
from af.pipeline.db import services as db_services
from af.pipeline.exceptions import AnalysisError

class AsremlRAnalyze(AsremlAnalyze):
    def run_job(self, job_data, analysis_engine=None):

        if not analysis_engine:
            analysis_engine = self.get_engine_script()

        job_dir = utils.get_parent_dir(job_data.data_file)

        job_detail = {
            "trait_name": job_data.trait_name,
            "location_name": job_data.location_name,
        }

        job = db_services.create_job(
            self.db_session,
            self.analysis.id,
            job_data.job_name,
            "IN-PROGRESS",
            "Processing in the input request",
            job_detail,
        )

        try:
            # TODO: Execute ASREMLR via RPy2?
            
            job = db_services.update_job(
                self.db_session, job, "IN-PROGRESS", "Completed the job. Pending post processing."
            )

            job_data.job_result_dir = job_dir

            return job_data
        except Exception as e:
            self.analysis.status = "FAILURE"
            db_services.update_job(self.db_session, job, "ERROR", str(e))
            utils.zip_dir(job_dir, self.output_file_path, job_data.job_name)
            raise AnalysisError(str(e))
        finally:
            self.db_session.commit()
