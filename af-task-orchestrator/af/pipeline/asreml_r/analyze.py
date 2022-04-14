from af.pipeline import utils
from af.pipeline.asreml.analyze import AsremlAnalyze
from af.pipeline.asreml_r.dpo import AsremlRProcessData  # temporary while we refactor parts
from af.pipeline.db import services as db_services
from af.pipeline.exceptions import AnalysisError
from af.pipeline.job_data import JobData

from rpy2.robjects.packages import importr
import rpy2.robjects as robjects


SCRIPT = '''
library(asreml)
# the input object just emulates a reqeuest and its data
input <- list(
  "request" = "{request_id}",
  "trait" = "AYLD_CONT",
  "formula_1job" = "{fixed_formula}",
  "formula_2job" = "fixed = {trait_name} ~ rep, random = ~ ge",
  "residual" = "{residual_formula}",
  "predict" = "ge"
)

data <- read.csv("{datafile}",h=T)

# Some data modification required by asreml (do not care with this now)
data <- data[with(data, order(occurrence,row,col)),]

# asreml requires that the data type of some columns are "factor"
data$rep <- as.factor(data$rep)
data$occurrence <- as.factor(data$occurrence)
data$expt <- as.factor(data$expt)
data$row <- as.factor(data$row)
data$col <- as.factor(data$col)
data$ge <- as.factor(data$ge)

# the multi-experiment should run, in the first stage, the analysis per occurrence
for(i in levels(data$occurrence)){
  data_occ <- data[data$occurrence==i,]
  data_occ <- droplevels(data_occ)
  
  # replacing the trait name in the formula of first job (ge as fixed)
  # input$formula_1job <- gsub("{trait_name}",replacement = input$trait,x = input$formula_1job,fixed=T)
  
  #creating the asreml call for the first job of the first stage
  asremlModel <-paste("asr <- asreml(",input$formula_1job,
                      ",residual=", input$residual,
                      ",data=data_occ)",
                      sep = "")

  
  #executing asreml
  eval(parse(text=asremlModel))
  
  # cicles until model gets converged
  tries <- 0
  while(!asr$converge & tries<6){
    tries <- tries+1
    asr<-update.asreml(asr)
  }
  
  #asreml generates many results, stored in the object we called asr, lets consider that we want the predictions
  
  #summary
  summary_model <- summary(asr)
  #predictions
  (pred <- predict.asreml(object = asr,classify = input$predict, sed = T))
  
  
  # printing RDS files with results (main asreml object -asr; its summary - summary; its prediction - pred)
  saveRDS(asr, paste("{job_dir}/{job_name}_asr}.rds", sep=""))
  saveRDS(summary_model, paste("{job_dir}/{job_name}_summary.rds", sep=""))
  saveRDS(pred, paste("{job_dir}/{job_name}_pred.rds", sep=""))
  
  # post analysis calculation - for calculation engine
  # vdBLUP.mat <- predict.asreml(asr, classify=input$predict, only=input$predict, sed=TRUE)$sed^2 # obtain squared s.e.d. matrix 
  # predict.asreml(asr, classify="ge", only="ge", sed=TRUE)$sed^2 # obtain squared s.e.d. matrix 
  # vdBLUP.avg <- mean(vdBLUP.mat[upper.tri(vdBLUP.mat, diag=FALSE)]) # take mean of upper triangle
  # vdBLUP.avg
  }
​
'''
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
    fixed_formula = str(job_data.job_params.formula)   
    # random_formula = "~ entry"
    residual_formula = job_data.job_params.residual
    # result1 = f"{job_dir}/{job_data.job_name}_results.csv"

    # replace trait_name in fixed formula
    fixed_formula = fixed_formula.format(
        trait_name=job_data.trait_name
    )

    user_script = SCRIPT.format(
        trait_name=job_data.trait_name,
        datafile=job_data.data_file,
        fixed_formula=fixed_formula,
        # random_formula=random_formula,
        residual_formula=residual_formula,
        job_dir=job_dir,
        job_name=job_data.job_name
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
    
    def process_job_result(self, job_result: JobData, gathered_objects: dict = None):
        return super().process_job_result(job_result, gathered_objects)
