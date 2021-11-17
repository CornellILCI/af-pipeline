from af.pipeline.analysis_request import AnalysisRequest
from af.pipeline.analyze import Analyze

from .dpo import SommeRProcessData


class SommeRAnalyze(Analyze):

    dpo_cls = SommeRProcessData
    engine_script = "rscript"

    def __init__(self, analysis_request: AnalysisRequest, *args, **kwargs):
        super().__init__(analysis_request=analysis_request, *args, **kwargs)

    
        
