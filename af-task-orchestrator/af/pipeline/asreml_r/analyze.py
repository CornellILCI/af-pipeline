from af.pipeline import utils
from af.pipeline.asreml.analyze import AsremlAnalyze
from af.pipeline.asreml_r.dpo import AsremlRProcessData  # temporary while we refactor parts
from af.pipeline.db import services as db_services
from af.pipeline.exceptions import AnalysisError
from af.pipeline.job_data import JobData

from rpy2.robjects.packages import importr
import rpy2.robjects as robjects


# TODO: This is a ME script ,  Pedro will provide script for single run
SCRIPT = '''
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

'''


def run_asremlr(job_dir, job_data: JobData, factors):
    """ 
    This function builds the R script that will be run.  The base script template is defined in SCRIPT var.
    """
    fixed_formula = str(job_data.job_params.formula) 
    residual_formula = job_data.job_params.residual
    prediction = job_data.job_params.predictions[0]
    trait_name = job_data.trait_name

    # replace trait_name in fixed formula
    if "{trait_name}" in fixed_formula:
        fixed_formula = fixed_formula.format(
            trait_name=trait_name
        )
      
    factor_script = ""
    for factor in factors:
        factor_script += f"data${factor} <- as.factor(data${factor})\n"

    user_script = SCRIPT.format(
        trait_name=trait_name,
        datafile=job_data.data_file,
        fixed_formula=fixed_formula,
        factor_script=factor_script,
        residual_formula=residual_formula,
        job_dir=job_dir,
        job_name=job_data.job_name,
        prediction=prediction
    )
    robjects.r(user_script)  # quickest way to implement, but might be hard to get error desc....


class AsremlRAnalyze(AsremlAnalyze):
    engine_script = "asreml-r"
    dpo_cls = AsremlRProcessData
    
    def run_job(self, job_data: JobData, analysis_engine=None):

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
            model_prop = db_services.get_property(self.db_session, self.analysis_request.analysisConfigPropertyId)
            # get factors for config and pass them
            factor_properties = db_services.get_child_properties(
                self.db_session, model_prop.code, model_prop.name
            )
            
            factors = [prop.code for prop in factor_properties if prop.data_type == "factor"]

            run_asremlr(job_dir, job_data, factors)
            
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
    
    def process_job_result(self, job_result: JobData, gathered_objects: dict = None):
        # TODO: customize job result processing
        # return super().process_job_result(job_result, gathered_objects)
        job_dir = utils.get_parent_dir(job_result.data_file)
        utils.zip_dir(job_dir, self.output_file_path, job_result.job_name)
        return gathered_objects

    def finalize(self, gathered_objects):
        return super().finalize(gathered_objects)

