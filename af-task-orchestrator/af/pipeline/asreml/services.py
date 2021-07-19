import xml.sax

from af.pipeline.asreml.resultparser import ASRemlContentHandler
from af.pipeline.db.core import DBConfig
from af.pipeline.db.models import FittedValues, ModelStat, Variance
from af.pipeline.asreml import yhatparser


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
    if ch.variances:
        session.bulk_insert_mappings(Variance, ch.variances)

    if ch.model_stat:
        # TODO: Remove the next two lines once we have them on db table
        ch.model_stat.pop("conclusion")
        ch.model_stat.pop("converged")

        model_stat = ModelStat(**ch.model_stat)

        session.add(model_stat)

    # TODO: add prediction row shere
    session.commit()


def process_yhat_result(session, job_id: int, filename_or_stream, *args, **kwargs):
    """Service func to process yhat files"""
    data = yhatparser.parse(filename_or_stream)
    data_dict = data.to_dict('records')

    for item in data_dict:
        item['job_id'] = job_id
        item['tenant_id'] = 1
        item['creator_id'] = 1

    if data_dict:
        session.bulk_insert_mappings(FittedValues, data_dict)
        session.commit()
