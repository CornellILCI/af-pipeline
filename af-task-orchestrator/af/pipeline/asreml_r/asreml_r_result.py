import numpy as np
import pandas as pd
import rpy2
from af.pipeline import db, rpy_utils

r_base = rpy2.robjects.packages.importr("base")


class AsremlRResult:

    # set of constant columns in all asreml-r prediction object.
    # help to figure out what are the variables that are predicted.
    predictions_const_columns = {"predicted.value", "std.error", "status"}

    # prediction object column names that needs to be renamed to standard report names.
    report_renname_columns = {"predicted.value": "value", "std.error": "std_error"}

    def __init__(self, job: db.models.Job, asr_rds_file: str, prediction_rds_files: list[str] = None):

        self.job = job

        self.asr = self.__read_asr(asr_rds_file)
        self.asr_summary = r_base.summary(self.asr)
        self.converged = AsremlRResult.is_converged(self.asr)
        self.model_stat = self.__parse_model_stat()
        if self.converged:
            self.__get_predictions_by_predictors(prediction_rds_files)
            self.variances = rpy_utils.rdf_to_pydf(self.asr_summary.rx2("varcomp"))

    def __read_asr(self, asr_rds_file):
        try:
            asr = r_base.readRDS(asr_rds_file)
            return asr
        except rpy2.rinterface_lib.embedded.RRuntimeError as e:
            raise RuntimeError("Unable to process asr result file")

    def __parse_model_stat(self):

        model_stat = dict()
        model_stat["log_lik"] = self.__read_robject_param(self.asr, "loglik")
        model_stat["aic"] = self.__read_robject_param(self.asr, "aic")
        model_stat["bic"] = self.__read_robject_param(self.asr, "bic")
        model_stat["is_converged"] = self.converged

        return model_stat

    def __read_robject_param(self, robj, param: str):

        value = robj.rx2(param)

        if value == rpy2.robjects.NULL:
            return None

        # values of robjects are vectors
        return list(value)[0]

    def __get_predictions_by_predictors(self, prediction_rds_files):

        self.__predictions_by_predictors = dict()
        self.__pvals_by_predictors = dict()
        self.__sed_by_predictors = dict()

        if not prediction_rds_files:
            return None

        for prediction_file in prediction_rds_files:

            try:
                predictions = r_base.readRDS(prediction_file)
            except rpy2.rinterface_lib.embedded.RRuntimeError as e:
                raise RuntimeError(f"Unable to process predictions result file {prediction_file}")

            if not predictions.rx2("pvals"):
                continue

            predictors = tuple(set(predictions.rx2("pvals").names) - self.predictions_const_columns)

            self.__predictions_by_predictors[predictors] = predictions

            pvals = rpy_utils.rdf_to_pydf(predictions.rx2("pvals"))
            pvals = pvals.rename(columns=self.report_renname_columns)
            pvals["job_id"] = self.job.id

            self.__pvals_by_predictors[predictors] = pvals

            sed = predictions.rx2("sed")

            if sed:
                self.__sed_by_predictors[predictors] = sed

    @property
    def entry_predictions(self) -> pd.DataFrame:
        predictor = tuple({"entry"})
        return self.__pvals_by_predictors.get(predictor)

    @property
    def location_predictions(self) -> pd.DataFrame:
        predictor = tuple({"loc"})
        return self.__pvals_by_predictors.get(predictor)

    @property
    def entry_location_predictions(self) -> pd.DataFrame:
        predictor = tuple({"entry", "loc"})
        return self.__pvals_by_predictors.get(predictor)

    @property
    def entry_variance(self) -> float:

        if self.variances is not None:
            return None
        try:
            return float(self.variances["component"]["entry"])
        except KeyError:
            return None

    @staticmethod
    def is_converged(asr):
        if asr:
            return bool(asr.rx2("converge"))
        return False

    @property
    def entry_average_standard_error(self) -> float:
        """
        from this r code,

        vmBLUP <- predR$sed ^ 2
        vmBLUP <- mean(vmBLUP[upper.tri(vmBLUP, diag = FALSE)], na.rm = T)

        """
        entry_predictor_key = tuple({"entry"})
        sed = self.__sed_by_predictors.get(entry_predictor_key)

        if not sed:
            return None

        sed_matrix = np.array(r_base.as_matrix(sed))

        # get upper triangle of sed matrix as array
        sed_upper_tri = sed_matrix[np.triu_indices(len(sed_matrix), 1)]

        # find the mean of their squares
        avg_std_error = np.mean(sed_upper_tri ** 2)

        return float(avg_std_error)
