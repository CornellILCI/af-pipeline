import pandas as pd
from af.pipeline import pandasutil, utils


REQUEST_INFO_SHEET_NAME = "Request Info"
ENTRY_SHEET_NAME = "Entry"
LOCATION_SHEET_NAME = "Location"
ENTRY_LOCATION_SHEET_NAME = "Entry x Location"
MODEL_STAT_SHEET_NAME = "Model Statistics"


REPORT_SHEETS = [
    REQUEST_INFO_SHEET_NAME,
    MODEL_STAT_SHEET_NAME,
    ENTRY_SHEET_NAME,
    LOCATION_SHEET_NAME,
    ENTRY_LOCATION_SHEET_NAME,
]


def write_predictions(report_file: str, predictions: list[dict], metadata_df: pd.DataFrame):
    """Writes spearate report sheet for predictions of entry, location and entry x location in
    the report workbook.
    Args:
        report_file: file path of the report to whcih predictions will be written.
        predictions: list of dictionary objects with following keys (* - indicates mandatory columns)
            job_id*: Id of the job which generated the predictions.
            entry: Id of the entry, if prediction is for entry
            loc: Id of the location, if the prediction is for location
            value*: Value of the prediction
            std_err*: Standard error for prediction
            num_factors*: Number of factors used by prediction
        metadata_df: DataFrame for metadata
            Index: RangeIndex
            Columns:
                entry_id: Id of the entry
                entry_name: Name of the entry
                entry_type: Type of the entry (example values: test, check)
                experiment_id: Id of the experiment
                experiment_name: Name of the experiment
                location: Name of the location
                location_id: Id of the location
                trait_abbreviation: Abbreviation of trait name
    """

    if len(predictions) == 0:
        return

    predictions_df = pd.DataFrame(predictions)

    # write entry report
    if "entry" in predictions_df.columns:
        write_entry_predictions(report_file, predictions_df, metadata_df)

    # write location report
    if "loc" in predictions_df.columns:
        write_location_predictions(report_file, predictions_df, metadata_df)

    # write entry and location report
    if "entry" in predictions_df.columns and "loc" in predictions_df.columns:
        write_entry_location_predictions(report_file, predictions_df, metadata_df)


def write_entry_predictions(report_file: str, predictions_df: pd.DataFrame, metadata_df: pd.DataFrame):

    entry_report_columns = [
        "job_id",
        "experiment_id",
        "experiment_name",
        "trait_abbreviation",
        "entry_id",
        "entry_name",
        "entry_type",
        "value",
        "std_error",
    ]

    # get entry only rows
    entry_report = predictions_df[predictions_df.entry.notnull()]
    entry_report = entry_report[entry_report.num_factors == 1]

    if len(entry_report) == 0:
        return

    entry_report = entry_report.merge(metadata_df, left_on="entry", right_on="entry_id")

    entry_report = entry_report[entry_report_columns]

    pandasutil.append_df_to_excel(report_file, entry_report, sheet_name=ENTRY_SHEET_NAME)


def write_location_predictions(report_file: str, predictions_df: pd.DataFrame, metadata_df: pd.DataFrame):

    location_report_columns = ["job_id", "trait_abbreviation", "location_id", "location_name", "value", "std_error"]

    location_df = metadata_df[["location_id", "location_name", "trait_abbreviation"]].drop_duplicates()

    # get location only rows
    # do not try to call loc column as property as it would conflict with default loc property
    location_report = predictions_df[predictions_df["loc"].notnull()]
    location_report = location_report[location_report.num_factors == 1]

    if len(location_report) == 0:
        return

    location_report = location_report.merge(location_df, left_on="loc", right_on="location_id")

    location_report = location_report[location_report_columns]

    pandasutil.append_df_to_excel(report_file, location_report, sheet_name=LOCATION_SHEET_NAME)


def write_entry_location_predictions(report_file: str, predictions_df: pd.DataFrame, metadata_df: pd.DataFrame):

    entry_location_report_columns = [
        "job_id",
        "trait_abbreviation",
        "entry_id",
        "entry_name",
        "location_id",
        "location_name",
        "value",
        "std_error",
    ]

    # get entry location only rows
    entry_location_report = predictions_df[predictions_df.entry.notnull()]
    entry_location_report = entry_location_report[entry_location_report["loc"].notnull()]
    entry_location_report = entry_location_report[entry_location_report.num_factors == 2]

    if len(entry_location_report) == 0:
        return

    entry_location_report = entry_location_report.merge(
        metadata_df, left_on=["entry", "loc"], right_on=["entry_id", "location_id"]
    )

    entry_location_report = entry_location_report[entry_location_report_columns]

    pandasutil.append_df_to_excel(report_file, entry_location_report, sheet_name=ENTRY_LOCATION_SHEET_NAME)


def write_model_stat(report_file: str, model_stat: dict, metadata_df: pd.DataFrame):

    # write model statistics
    if len(model_stat) == 0:
        return

    model_stats_df = pd.DataFrame([model_stat])

    model_stats_report_columns = [
        "job_id",
        "experiment_name",
        "trait_abbreviation",
        "location_name",
        "log_lik",
        "aic",
        "bic",
        "components",
        "conclusion",
        "is_converged",
    ]

    model_stats_df["experiment_name"] = ",".join(metadata_df.experiment_name.drop_duplicates().astype(str))
    model_stats_df["location_name"] = ",".join(metadata_df.location_name.drop_duplicates().astype(str))
    model_stats_df["trait_abbreviation"] = ",".join(metadata_df.trait_abbreviation.drop_duplicates().astype(str))

    model_stats_df = pandasutil.df_keep_columns(model_stats_df, model_stats_report_columns)

    pandasutil.append_df_to_excel(report_file, model_stats_df, sheet_name=MODEL_STAT_SHEET_NAME)
