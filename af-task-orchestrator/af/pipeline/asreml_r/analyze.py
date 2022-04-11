from af.pipeline import utils
from af.pipeline.asreml.analyze import AsremlAnalyze  # temporary while we refactor parts
from af.pipeline.db import services as db_services
from af.pipeline.exceptions import AnalysisError
from af.pipeline.job_data import JobData

from rpy2.robjects.packages import importr
import rpy2.robjects as robjects

script = '''
library(asreml)

# just using the example data
data <- read.csv("{datafile}",h=T)

# Some cata modification required by asreml (do not care with this now)
data <- data[with(data, order(row,col)),]
data$rep <- as.factor(data$rep)
data$row <- as.factor(data$row)
data$col <- as.factor(data$col)
data$entry <- as.factor(data$entry)

# stat model (the pipeline will provide this from the ba)
# here is where asreml is really executed
asr <- asreml(fixed = {fixed_formula},
              random = {random_formula},
              residual = {residual_formula},
              data = data)

#requested result
#asreml generates many results, stored in the object we called asr, lets consider that we want the predictions 
pred<-predict(asr,classify="entry")$pvals

#printing the results in a csv (we may not do this way in our pipeline)
write.csv(pred, file = "{result1}",quote=F,row.names=F)

'''


def run_asremlr(job_dir, job_data: JobData):
    
    fixed_formula = job_data.job_params.formula
    random_formula = "~ entry"
    residual_formula = job_data.job_params.residual
    result1 = f"{job_dir}/results.csv"

    user_script = script.format(
        datafile=job_data.data_file,
        fixed_formula=fixed_formula,
        random_formula=random_formula,
        residual_formula=residual_formula,
        result1=result1
    )

    robjects.r(user_script)  # quickest way to implement, but might be hard to get error desc....


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
            run_asremlr(job_dir, job_data)
            
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
