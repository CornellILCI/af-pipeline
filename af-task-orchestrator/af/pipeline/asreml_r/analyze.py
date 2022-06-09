import collections
import pathlib
from dataclasses import dataclass, field
from os import path

import rpy2
import rpy2.robjects as robjects
from af.pipeline import analysis_report, rpy_utils, utils, calculation_engine
from af.pipeline.asreml.analyze import AsremlAnalyze
from af.pipeline.asreml_r.asreml_r_result import AsremlRResult
from af.pipeline.asreml_r.dpo import AsremlRProcessData  # temporary while we refactor parts
from af.pipeline.db import services as db_services
from af.pipeline.exceptions import AnalysisError
from af.pipeline.job_data import JobData
from af.pipeline.job_status import JobStatus
from rpy2.robjects import pandas2ri
from rpy2.robjects.conversion import localconverter

# TODO: This is a ME script ,  Pedro will provide script for single run
SCRIPT = """
library(asreml)
# the input object just emulates a reqeuest and its data
input <- list(
  "request" = "{job_name}",
  "trait" = "{trait_name}",
  "formula_1job" = "{fixed_formula}",
  #"formula_2job" = "fixed = {trait_name} ~ rep, random = ~ ge",
  "residual" = "{residual_formula}",
  "options" = "na.action = na.method(y = 'include', x = 'include')",
  "predict" = "{prediction}"
)

data <- read.csv("{datafile}",h=T)

# Some data modification required by asreml (do not care with this now)
data <- data[with(data, order(row,col)),]

# asreml requires that the data type of some columns are "factor"
{factor_script}

#creating the asreml call for the first job of the first stage
asremlModel <-paste("asr <- asreml(",input$formula_1job,
                    ",residual=", input$residual,
                    ",",input$options,
                    ",data=data)",
                    sep = "")


#executing asreml
eval(parse(text=asremlModel))

# cicles until model gets converged
tries <- 0
while(!asr$converge & tries<6){{
tries <- tries+1
asr<-update.asreml(asr)
}}

#asreml generates many results, stored in the object we called asr, lets consider that we want the predictions

#summary
summary_model <- summary(asr)
#predictions
(pred <- predict.asreml(object = asr,classify = input$predict, sed = T))


# printing RDS files with results (main asreml object -asr; its summary - summary; its prediction - pred)
saveRDS(asr, paste("{job_dir}/{job_name}_asr.rds", sep=""))
saveRDS(summary_model, paste("{job_dir}/{job_name}_summary.rds", sep=""))
saveRDS(pred, paste("{job_dir}/{job_name}_pred.rds", sep=""))

"""


@dataclass
class AsremlRJobResult(JobData):
    asr_rds_file: str = ""
    prediction_rds_files: list[str] = field(default_factory=list)


class AsremlRAnalyze(AsremlAnalyze):

    engine_script = "asreml-r"
    dpo_cls = AsremlRProcessData

    asr_rds_file_name = "asr.rds"
    prediction_rds_file_name = "prediction{i}.rds"

    CONVERGENCE_TRIES = 6

    @robjects.packages.no_warnings
    def run_job(self, job_data: JobData):

        job_dir = utils.get_parent_dir(job_data.data_file)
        job = db_services.create_job(
            self.db_session,
            self.analysis.id,
            job_data.job_name,
            JobStatus.INPROGRESS,
            "Processing input request",
            {},
        )

        r_base = robjects.packages.importr("base")

        input_data = rpy_utils.read_csv(file=job_data.data_file)

        # set data types to input data fields
        # ASReml-R has only two datatypes, factor & numeric
        # datatype keys are lower case
        datatype_converters = {"factor": r_base.as_factor, "numeric": r_base.as_numeric}
        if job_data.job_params.analysis_fields_types:
            for field in job_data.job_params.analysis_fields_types:

                data_type = job_data.job_params.analysis_fields_types.get(field)
                converter = datatype_converters.get(data_type)

                if converter:
                    input_data[input_data.colnames.index(field)] = converter(input_data.rx2(field))

        # asreml has fixed, random and residual formulas.
        model_formulas = {}

        fixed = rpy_utils.r_formula(job_data.job_params.fixed)
        if fixed is not None:
            model_formulas["fixed"] = fixed

        random = rpy_utils.r_formula(job_data.job_params.random)
        if random is not None:
            model_formulas["random"] = random

        residual = rpy_utils.r_formula(job_data.job_params.residual)
        if residual is not None:
            model_formulas["residual"] = residual

        asr_rds_file = utils.path_join(job_dir, self.asr_rds_file_name)

        asr = None
        prediction = None

        job_result = AsremlRJobResult(**job_data.__dict__)

        try:

            # license gets checked out when asreml is imported
            asreml_r = robjects.packages.importr("asreml")

            asr = asreml_r.asreml(
                **model_formulas, data=input_data, na_action=asreml_r.na_method(y="include", x="include")
            )

            if asr:

                # try to converge by updating asr
                tries = 0
                while AsremlRResult.is_converged(asr) == False and tries < CONVERGENCE_TRIES:
                    asr = asreml_r.update(asr, **model_formulas)
                    tries += 1

                # save asr as rds file
                r_base.saveRDS(asr, asr_rds_file)

                job_result.asr_rds_file = asr_rds_file

                # run predictions
                for i, prediction_statement in enumerate(job_data.job_params.predictions):
                    prediction = asreml_r.predict_asreml(
                        object=asr, classify=prediction_statement, sed=True, **model_formulas
                    )
                    prediction_rds_file = utils.path_join(job_dir, self.prediction_rds_file_name.format(i=i + 1))
                    r_base.saveRDS(prediction, prediction_rds_file)

                    job_result.prediction_rds_files.append(prediction_rds_file)

            # checking in the license back
            r_base.detach("package:asreml", unload=True)

        except (rpy2.rinterface_lib.embedded.RRuntimeError, ValueError) as e:
            self.analysis.status = "FAILURE"
            db_services.update_job(self.db_session, job, JobStatus.ERROR, str(e))
            utils.zip_dir(job_dir, self.output_file_path, job.name)
            raise AnalysisError(str(e))

        job_result.job_result_dir = job_dir

        return job_result

    @robjects.packages.no_warnings
    def process_job_result(self, job_result: AsremlRJobResult, gathered_objects: dict = None):

        job = db_services.get_job_by_name(self.db_session, job_result.job_name)

        asreml_result = AsremlRResult(job, job_result.asr_rds_file, job_result.prediction_rds_files)

        if not asreml_result.converged:
            db_services.update_job(
                self.db_session,
                job,
                JobStatus.FAILED,
                "Failed to converge.",
            )
            return gathered_objects

        # initialize the report workbook
        if not path.isfile(self.report_file_path):
            utils.create_workbook(self.report_file_path, sheet_names=analysis_report.REPORT_SHEETS)

        metadata_df = utils.get_metadata(job_result.metadata_file)

        # write entry predictions to the report
        if asreml_result.entry_predictions is not None:
            analysis_report.write_entry_predictions(
                self.db_session,
                self.analysis_request,
                self.report_file_path,
                asreml_result.entry_predictions,
                metadata_df,
            )

        # write location predictions to the report if
        if asreml_result.location_predictions is not None:
            analysis_report.write_location_predictions(
                self.report_file_path, asreml_result.location_predictions, metadata_df
            )

        # write entry location predictions
        if asreml_result.entry_location_predictions is not None:
            analysis_report.write_entry_location_predictions(
                self.report_file_path, asreml_result.entry_location_predictions, metadata_df
            )

        # calculate h2 cullis for entry if analysis pattern is SESL
        h2_cullis = None
        exptloc_analysis_pattern = db_services.get_property(
            self.db_session, self.analysis_request.expLocAnalysisPatternPropertyId
        )

        if exptloc_analysis_pattern.code == "SESL":

            variance = asreml_result.entry_variance
            avg_std_error = asreml_result.entry_average_standard_error

            if variance is not None and avg_std_error is not None:
                try:
                    h2_cullis = calculation_engine.get_h2_cullis(variance, avg_std_error)
                except ValueError as ve:
                    h2_cullis = str(ve)

        # write model statisics to analysis report
        rename_keys = {"log_lik": "LogL"}
        analysis_report.write_model_stat(
            self.report_file_path, asreml_result.model_stat, metadata_df, rename_keys, h2_cullis=h2_cullis
        )

        utils.zip_dir(job_result.job_result_dir, self.output_file_path, job_result.job_name)

        # TODO: below code duplicates from base class. can be reformated.
        db_services.update_job(self.db_session, job, JobStatus.FINISHED, "LogL converged")

        # gather occurrences from the jobs, so we don't have to read occurrences again.
        # will not work for parallel jobs. For parallel job, gather will happen in finalize
        if "occurrences" not in gathered_objects:
            gathered_objects["occurrences"] = {}

        for occurrence in job_result.occurrences:
            if occurrence.occurrence_id not in gathered_objects["occurrences"]:
                gathered_objects["occurrences"][occurrence.occurrence_id] = occurrence

        self.db_session.commit()
        return gathered_objects

    def finalize(self, gathered_objects):
        return super().finalize(gathered_objects)
