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
    ch = ASRemlContentHandler()
    parser.setContentHandler(ch)
    parser.parse(filename_or_stream)

    # process the objects
    if ch.variances:
        for var in ch.variances:
            var["job_id"] = job_id

            # TODO: fake tenant_id, creator_id -- remove these later
            var["tenant_id"] = 1
            var["creator_id"] = 1
            
            variance = Variance(**var)
            session.add(variance)

    if ch.model_stat:
        ch.model_stat["job_id"] = job_id
        # NOTE: Remove converged and conclusion for now until they exist in model_stat table
        # TODO: remote the next two lines
        ch.model_stat.pop("conclusion")
        ch.model_stat.pop("converged")

        # TODO: fake tenant_id, creator_id -- remove these later
        ch.model_stat["tenant_id"] = 1
        ch.model_stat["creator_id"] = 1

        model_stat = ModelStat(**ch.model_stat)
        session.add(model_stat)

    session.commit()    
