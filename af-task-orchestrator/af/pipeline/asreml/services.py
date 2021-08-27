import xml.sax

from datetime import datetime

from af.pipeline.asreml.resultparser import ASRemlContentHandler
from af.pipeline.db.core import DBConfig
from af.pipeline.db.models import FittedValues, ModelStat, Prediction, ResidualOutlier, Variance
from af.pipeline.asreml import yhatparser, resparser


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
    parser.parse(filename_or_stream)

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


def _save_variances(session, variances):
    if variances:
        session.bulk_insert_mappings(Variance, variances)


def _save_predictions(session, predictions):
    if predictions:
        session.bulk_insert_mappings(Prediction, predictions)


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

def save_residual_outlier(session, job_id:int, filename):
    
    outliers = resparser.parse_res(resparser.check_file(filename))

    data_dict = {}

    for outlier in outliers:
        data_dict["job_id"] = job_id
        data_dict["outlier"] = outlier
    if data_dict:
        session.bulk_insert_mappings(ResidualOutlier, data_dict)
        session.commit()
    