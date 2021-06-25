import xml.sax

from pipeline.asreml.resultparser import ASRemlContentHandler
from pipeline.db.models import ModelStat, Variance


def get_file_parser():
    parser = xml.sax.make_parser()
    parser.setFeature(xml.sax.handler.feature_namespaces, 0)
    return parser


def process_asreml_result(session, job_id: int, filename_or_stream, *args, **kwargs):
    """Service func to process asreml result and save to db"""

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
