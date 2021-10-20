
import csv
from af.pipeline.exceptions import FileParseException
from af.pipeline.db.models import ModelStat, Prediction

SOMMER_PREDICTION_COLUMNS_TO_DB_COLUMNS = {
    "trait": "trait_value",
    "ID": "id",
    "predicted.value": "value",
    "standard.error": "std_error",
}
SOMMER_MODEL_STAT_COLUMNS_TO_DB_COLUMNS = {
    "logLik": "log_lik",
    "AIC": "aic",
    "BIC": "bic",
    "Method": "method_id",
    "Converge": "is_converged"
}

static = ["record", "yhat", "residual", "hat"]

def get_model_stat(job_id: int, model_stat_result_file_path: str): 
    """
    Creates a Model Stat sqlalchemy object, by parsing the input sommer result file. Model Stat model is already defined in db models.
    """

    try:
        prediction_data = csv.DictReader(open(model_stat_result_file_path))
        for row in prediction_data:
            row = {SOMMER_MODEL_STAT_COLUMNS_TO_DB_COLUMNS[name]: val for name, val in row.items()}
            model_stat_object = ModelStat(**row)
        return model_stat_object

    except Exception as exc:
        raise FileParseException(exc)   

def get_prediction(job_id: int, prediction_result_file_path: str):

    """
    Creates a list of Prediction sqlalchemy objects, by parsing the input sommer result file. Prediction model is already defined in db models.
    """
    try:

        prediction_data = csv.DictReader(open(prediction_result_file_path))
        prediction_object_list = []

        for row in prediction_data:
            row = {SOMMER_PREDICTION_COLUMNS_TO_DB_COLUMNS[name]: val for name, val in row.items()}
            prediction = Prediction(**row)
            prediction_object_list.append(prediction)
        return prediction_object_list

    except Exception as exc:

        raise FileParseException(exc)
