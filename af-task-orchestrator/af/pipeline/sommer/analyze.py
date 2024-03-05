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
    prediction_rds_files: 'list[str]' = field(default_factory=list)


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
        try:
            return super().pre_process()
        #If we've failed in pre-processing, we do need to drop a 'job' so we can fail
        #gracefully instead of infinitely retrying
        except Exception as e:
            db.services.create_job(
            self.db_session,
            self.analysis.id,
            "Does name really matter?",
            JobStatus.ERROR,
            str(e),
            {},) 
            return 

    #Return a 'pure R' version of the run script. 
    #This needs to be updated when the analysis changes, but it's better than
    #rewriting this whole thing in pure R, but still lets an end-user get a 
    #re-runnable representation of what happened. Bit of a hack. -Josh L.S.
    @robjects.packages.no_warnings
    def job_as_Rscript(self, job_data):
        job_dir = utils.get_parent_dir(job_data.data_file)
        
        script = f"""
        #install.packages('sommer')
        #install.packages('readr')
        
        input_data<-read.csv(file='{job_data.data_file}',sep=',',header=TRUE)
        input_data$rep <- as.factor(input_data$rep)
        input_data$genotype <- as.factor(input_data$genotype)
        """
        #Placing variables 'in line' instead of in a kwargs... couldn't find a good substitute, given these are commands, not
        #strings. -JDLS
        script += f"""mix1 <- mmer(
            fixed= {rpy_utils.r_formula(job_data.job_params.fixed).r_repr().strip()},
            random= {rpy_utils.r_formula(job_data.job_params.random).r_repr().strip()},
            rcov= {rpy_utils.r_formula(job_data.job_params.residual).r_repr().strip()},
            data= input_data)
        """
        result_rds_file = utils.path_join(job_dir, self.sommer_rds_file_name)
        script += f"""saveRDS(mix1, '{result_rds_file}')
        """
            # run predictions
        for i, prediction_statement in enumerate(job_data.job_params.predictions):

            prediction_rds_file = utils.path_join(job_dir, self.prediction_rds_file_name.format(i=i + 1))
            script += f"""predictions <- predict.mmer(object=mix1, classify='{prediction_statement}')
    saveRDS(predictions,'{prediction_rds_file}')
            """

            return script


    @robjects.packages.no_warnings
    def run_job(self, job_data:JobData):

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

        #if we contain an R 'factor' type - such as 'rep', import_csv will treat it as continuous
        #Effectively we need to do - input_data$rep <- as.factor(input_data$rep)
        input_data = rpy_utils.factorize(input_data,'rep')  
        input_data = rpy_utils.factorize(input_data,'genotype')
        #Copy a 'pure R' version of this script into the output directory
        script_path = utils.path_join(job_dir,"script.r")#R script path
        script_handle=open(script_path,"w")
        script_handle.write(self.job_as_Rscript(job_data))
        script_handle.close()
        
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

    

    @robjects.packages.no_warnings
    def process_job_result(self, job_result: JobData, gathered_objects: dict = None):

        job = db.services.get_job_by_name(self.db_session, job_result.job_name)

        # lot of duplicacy between below code and asreml_r_result. They can be modularized.
        r_base = rpy2.robjects.packages.importr("base")

        sommer_result = r_base.readRDS(job_result.result_rds_file)

        if not (sommer_result or bool(sommer_result.rx2("convergence"))):
            db.services.update_job(
                self.db_session,
                job,
                JobStatus.FAILED,
                "Failed to converge.",
            )
            return gathered_objects

        # summary
        sommer_result_summary = r_base.summary(sommer_result)

        # TODO: Need to find a way to replace all hardcoded variable names like U, PevU, genotype.
        # Not sure if it is only entry that the end users are interested in!

        # write variances
        variances = sommer_result_summary.rx2("varcomp")
        variances_file_path = utils.path_join(job_result.job_result_dir, "variances")
        rpy_utils.rdf_to_csv(variances, variances_file_path)

        #
        #   #outliers
        #   out <- boxplot.stats(Residuals)$out
        #   if(length(out)>0){
        #     outliers <- inputData[Residuals%in%out,]
        #     rownames(outliers)
        #     write.csv(outliers, file=jsonInput$output_outliers, row.names = F, quote=F)
        #   }

        # write sln file
        breeding_values_file_path = utils.path_join(job_result.job_result_dir, "breeding_values")
        breeding_values = r_base.as_data_frame(sommer_result.rx2("U").rx2("genotype").rx2(job_result.trait_name))
        breeding_values.colnames = "breeding_values"
        breeding_values.std_error = r_base.sqrt(
            r_base.diag(sommer_result.rx2("PevU").rx2("genotype").rx2(job_result.trait_name))
        )
        breeding_values_sln = r_base.data_frame(
            genotype=r_base.rownames(breeding_values),
            breeding_values=breeding_values,
            std_error=breeding_values.std_error,
        )
        rpy_utils.rdf_to_csv(breeding_values_sln, breeding_values_file_path)
        
        residuals = sommer_result.rx2('residuals')

        # write yhat
        yhat_file_path = utils.path_join(job_result.job_result_dir, "y_hat")
        y_hat = sommer_result.rx2('fitted')
        hat = r_base.diag(sommer_result.rx2('P'))
        fitted = r_base.as_data_frame(r_base.cbind(y_hat, residuals, hat))
        fitted.colnames = r_base.c("Yhat", "Residuals", "Hat")
        rpy_utils.rdf_to_csv(fitted, yhat_file_path)
        
        # TODO: Adding outliers is pending. It needs more explanation from req analysts about the operators
        # used

        db.services.update_job(self.db_session, job, JobStatus.FINISHED, "LogL converged")

        utils.zip_dir(job_result.job_result_dir, self.output_file_path, job_result.job_name)

    def finalize(self, gathered_objects):
        pass
