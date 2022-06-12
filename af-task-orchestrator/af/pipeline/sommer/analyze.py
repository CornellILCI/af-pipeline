import rpy2
import rpy2.robjects as robjects
from rpy2.robjects import packages as r_packages

from af.pipeline.analysis_request import AnalysisRequest
from af.pipeline.analyze import Analyze
from af.pipeline.job_data import JobData
from af.pipeline.job_status import JobStatus

from af.pipeline import utils, db, rpy_utils
from dataclasses import dataclass, field
from af.pipeline.exceptions import AnalysisError

from .dpo import SommeRProcessData


@dataclass
class SommeRJobResult(JobData):
    result_rds_file: str = ""
    prediction_rds_files: list[str] = field(default_factory=list)


class SommeRAnalyze(Analyze):

    dpo_cls = SommeRProcessData
    engine_script = "sommer"
    sommer_rds_file_name = "result.rds"
    prediction_rds_file_name = "prediction{i}.rds"

    def __init__(self, analysis_request: AnalysisRequest, *args, **kwargs):
        super().__init__(analysis_request=analysis_request, *args, **kwargs)

    def get_cmd(self, job_data, analysis_engine=None):
        return ["sommer", job_data.job_file]

    def pre_process(self):
        return super().pre_process()

    @robjects.packages.no_warnings
    def run_job(self, job_data):

        job_dir = utils.get_parent_dir(job_data.data_file)
        job = db.services.create_job(
            self.db_session,
            self.analysis.id,
            job_data.job_name,
            JobStatus.INPROGRESS,
            "Processing input request",
            {},
        )

        job_result = SommeRJobResult(**job_data.__dict__)

        result_rds_file = utils.path_join(job_dir, self.sommer_rds_file_name)
        r_base = r_packages.importr("base")

        model_formulas = {}

        model_formulas["fixed"] = rpy_utils.r_formula(job_data.job_params.fixed)
        model_formulas["random"] = rpy_utils.r_formula(job_data.job_params.random)
        model_formulas["rcov"] = rpy_utils.r_formula(job_data.job_params.residual)

        input_data = rpy_utils.read_csv(file=job_data.data_file)
        try:
            sommer = r_packages.importr("sommer")

            mix1 = sommer.mmer(**model_formulas, data=input_data)

            r_base.saveRDS(mix1, result_rds_file)

            job_result.result_rds_file = result_rds_file

            # run predictions
            for i, prediction_statement in enumerate(job_data.job_params.predictions):

                predictions = sommer.predict_mmer(object=mix1, classify=prediction_statement)
                
                prediction_rds_file = utils.path_join(job_dir, self.prediction_rds_file_name.format(i=i + 1))
                r_base.saveRDS(predictions, prediction_rds_file)
                job_result.prediction_rds_files.append(prediction_rds_file)
            

        except (rpy2.rinterface_lib.embedded.RRuntimeError, ValueError) as e:
            self.analysis.status = "FAILURE"
            db.services.update_job(self.db_session, job, JobStatus.ERROR, str(e))
            utils.zip_dir(job_dir, self.output_file_path, job.name)
            raise AnalysisError(str(e))

        job_result.job_result_dir = job_dir
        return job_result

    def process_job_result(self, job_result: JobData, gathered_objects: dict = None):
        
        job = db.services.get_job_by_name(self.db_session, job_result.job_name)

        # lot of duplicacy between below code and asreml_r_result. They can be modularized.
        r_base = rpy2.robjects.packages.importr("base")

        sommer_result = r_base.readRDS(job_result.result_rds_file)
        
        if not (sommer_result or bool(sommer_result.rx2('convergence'))):
            db.services.update_job(
                self.db_session,
                job,
                JobStatus.FAILED,
                "Failed to converge.",
            )
            return gathered_objects

        db.services.update_job(self.db_session, job, JobStatus.FINISHED, "LogL converged")

        utils.zip_dir(job_result.job_result_dir, self.output_file_path, job_result.job_name)

    def finalize(self, gathered_objects):
        pass
