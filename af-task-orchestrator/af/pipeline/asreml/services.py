import io
import re
import xml.sax
from datetime import datetime

from af.pipeline import utils as pipeline_utils
from af.pipeline.asreml import stupid_asreml_xml_resolver, yhatparser
from af.pipeline.asreml.resultparser import ASRemlContentHandler
from af.pipeline.db.core import DBConfig
from af.pipeline.db.models import FittedValues, ModelStat, PredictionEffect, Variance


def get_file_parser():
    parser = xml.sax.make_parser()
    parser.setFeature(xml.sax.handler.feature_namespaces, 0)
    return parser


def process_asreml_result(session, job_id: int, filename_or_stream, *args, **kwargs):
    """Service func to process asreml result and save to db"""
    if not session:
        session = DBConfig.get_session()

    parser = get_file_parser()
    ch = ASRemlContentHandler(job_id)
    parser.setContentHandler(ch)

    resolved_xml_string = None

    try:
        parser.parse(filename_or_stream)
    except xml.sax.SAXParseException:
        # try resolving the predict table mismatched tags
        resolved_xml_string = stupid_asreml_xml_resolver.resolve_unmatched_tags(filename_or_stream)

    if resolved_xml_string:
        parser.parse(io.StringIO(resolved_xml_string))

    # process the objects
    if ch.model_stat:
        model_stat = ModelStat(**ch.model_stat)

        model_stat.job_id = job_id
        model_stat.tenant_id = 1
        model_stat.creator_id = 1
        model_stat.creation_timestamp = datetime.utcnow()

        session.add(model_stat)

        if model_stat.is_converged:
            _save_variances(session, ch.variances)
            _save_predictions(session, ch.predictions)

    session.commit()

    return ch


def get_average_std_error(pvs_file: str) -> float:
    """Reads the pvs_file from asreml result and calculates average standard error.

        Input file has predictions and a symmetirc matrix with errors
        for each prediction. Symmetric matrix is represented in the file are wrapped for some row length. For example,

        1
        1 1
        1 1 1
        1 1 1 1
        1 1 1 1 1

        is written as

        1
        1 1
        1 1 1
        1 1 1
        1
        1 1 1
        1 1

        The above matrix is wrapped for row length of 3. The method unwraps them to remove prediction_id from the
        calculation.

        average standard error = sum_of(square_of_all(cells in symmetric_matrix)) divided_by total_number_of_values

        Uses the line, 'Predicted values with SED(PV)' to identify the beggining of symmetric matrix.

    Args:
        pvs_file: pvs file path.

    Returns:
        Float value. Average stanadard error

    Raises:
        ValueError: when the input file path is invalid.

    """
    if not pipeline_utils.is_valid_file(pvs_file):
        raise ValueError("SE Blup Calculation: PVS file not found in ASReml results.")

    # flag to say whether to read the values in the file or not
    read = False

    # pattern to stop reading when non numeric values found in line
    alphabets_pattern = re.compile("[a-zA-Z]")

    # to keep index of column of symmetric matrix
    column = 0

    # increments after reading each row as it is symmetric matrix
    row_len = 1

    total_sum = 0  # sum of square of all seds
    total_count = 0  # number of seds

    tokens = {" ", "\n"}

    std_avg_error = 0.0

    with open(pvs_file) as f:

        for line in f:

            if "Predicted values with SED(PV)" in line:
                read = True
                continue
            elif read and bool(alphabets_pattern.search(line)):
                break

            # read only when conditions checked
            if read:
                sed = ""
                for c in line:
                    if c not in tokens:
                        sed += c
                    elif sed:
                        # skip first column
                        if column > 0:
                            sed_numeric = float(sed)
                            total_sum += sed_numeric ** 2
                            total_count += 1

                        column += 1

                        # when row length reached, reset column index and increase next row length by 1
                        if column == row_len:
                            column = 0
                            row_len += 1
                        sed = ""
    if total_count > 0:
        std_avg_error = total_sum / total_count
    return std_avg_error


def _save_variances(session, variances):
    if variances:
        session.bulk_insert_mappings(Variance, variances)


def _save_predictions(session, predictions):
    if predictions:
        session.bulk_insert_mappings(PredictionEffect, predictions)


def process_yhat_result(session, job_id: int, filename_or_stream, *args, **kwargs):
    """Service func to process yhat files"""
    data = yhatparser.parse(filename_or_stream)
    data_dict = data.to_dict("records")
    for item in data_dict:
        item["job_id"] = job_id
        item["tenant_id"] = 1
        item["creator_id"] = 1

    if data_dict:
        session.bulk_insert_mappings(FittedValues, data_dict)
        session.commit()
