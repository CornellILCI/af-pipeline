import rpy2
import rpy2.robjects as robjects

from af.pipeline.analysis_request import AnalysisRequest
from af.pipeline.analyze import Analyze
from af.pipeline.job_data import JobData

from af.pipeline import utils, db

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
        super().pre_process()

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

        r_base = robjects.packages.importr("base")

        model_formulas = {}

        model_formulas["fixed"] = rpy_utils.r_formula(job_data.job_params.fixed)
        model_formulas["random"] = rpy_utils.r_formula(job_data.job_params.random)
        model_formulas["rcov"] = rpy_utils.r_formula(job_data.job_params.residual)

        input_data = rpy_utils.read_csv(file=job_data.data_file)

        sommer = robjects.packages.importr("sommer")

        mix1 = sommer.mmer(**model_formulas, data=input_data, sep="")

        r_base.saveRDS(mix1, result_rds_file)

        job_result.result_rds_file = result_rds_file

        # run predictions
        for i, prediction_statement in enumerate(job_data.job_params.predictions):

            predictions = sommer.predict_mmer(object=mix1, classify=prediction_statement)
            prediction_rds_file = utils.path_join(job_dir, self.prediction_rds_file_name.format(i=i + 1))
            r_base.saveRDS(predictions, prediction_rds_file)

            job_result.prediction_rds_files.append(prediction_rds_file)

        job_result.job_result_dir = job_dir
        return job_result

    def process_job_result(self, job_result: JobData, gathered_objects: dict = None):
        pass

    def finalize(self, gathered_objects):
        pass
