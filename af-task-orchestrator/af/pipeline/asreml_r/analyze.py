import rpy2.robjects as robjects
from af.pipeline import rpy_utils, utils, job_status
from af.pipeline.asreml.analyze import AsremlAnalyze
from af.pipeline.asreml_r.dpo import AsremlRProcessData  # temporary while we refactor parts
from af.pipeline.db import services as db_services
from af.pipeline.exceptions import AnalysisError
from af.pipeline.job_data import JobData
from af.pipeline import rpy_utils
import rpy2
import rpy2.robjects as robjects

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


class AsremlRAnalyze(AsremlAnalyze):

    engine_script = "asreml-r"
    dpo_cls = AsremlRProcessData

    @robjects.packages.no_warnings
    def run_job(self, job_data: JobData):

        job = db_services.create_job(
            self.db_session,
            self.analysis.id,
            job_data.job_name,
            job_status.JobStatus.INPROGRESS,
            "Processing input request",
            {},
        )

        input_data = rpy_utils.read_csv(file=job_data.data_file)

        asreml_r = robjects.packages.importr("asreml")
        
        asr = asreml_r.asreml(
            robjects.Formula(job_data.job_params.formula),
            residual=robjects.Formula(job_data.job_params.residual),
            data=input_data
        )

        return JobData()

    def process_job_result(self, job_result: JobData, gathered_objects: dict = None):
        # TODO: customize job result processing
        # return super().process_job_result(job_result, gathered_objects)
        job_dir = utils.get_parent_dir(job_result.data_file)
        utils.zip_dir(job_dir, self.output_file_path, job_result.job_name)
        return gathered_objects

    def finalize(self, gathered_objects):
        return super().finalize(gathered_objects)
