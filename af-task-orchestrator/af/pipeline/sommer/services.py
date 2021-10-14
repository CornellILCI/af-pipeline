import pandas as pd
import csv
from af.pipeline.exceptions import FileParseException
from af.pipeline.db.models import ModelStat, Prediction

SOMMER_PREDICTION_COLUMNS_TO_DB_COLUMNS = { "trait": "trait_value",
                                            "ID": "id",
                                            "predicted.value": "value",
                                            "standard.error": "std_error"}
SOMMER_MODEL_STAT_COLUMNS_TO_DB_COLUMNS = {"sommer name as key": "db name as val"}

static = ["record", "yhat", "residual", "hat"]

hard_coded_input = "/home/vince/Documents/work/BA-726/output_pred.csv"
hard_coded_input = "/home/vince/Documents/work/BA-726/output_statmodel.csv"


def get_prediction(job_id: int , prediction_result_file_path:  str):
    """
    Creates a list of Prediction sqlalchemy objects, by parsing the input sommer result file. Prediction model is already defined in db models.
    """
    try:
        prediction_data = csv.DictReader(open(prediction_result_file_path))
        for row in prediction_data:
            row = {SOMMER_PREDICTION_COLUMNS_TO_DB_COLUMNS[name]: val for name, val in row.items()}
            print(row)
        prediction_object_list = [Prediction(**d) for d in prediction_data]
        return prediction_object_list

    except Exception as exc: 

        raise FileParseException(exc)



# def get_model_stat(job_id: int, model_stat_result_file_path: str):
#     """
#     Creates model_stat sqlalchemy object by parsing the result file for model_stat.
#     """
#     try:
#         df = pd.read_csv(model_stat_result_file_path, delimiter=r"\s+")
#         df.rename(columns=SOMMER_MODEL_STAT_COLUMNS_TO_DB_COLUMNS, inplace=True)
    
#     except Exception as exc:

#         raise FileParseException(exc)
    
#     return ModelStat