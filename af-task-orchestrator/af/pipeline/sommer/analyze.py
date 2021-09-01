from .dpo import SommeRProcessData
from af.pipeline.analyze import Analyze


class SommeRAnalyze(Analyze):

    dpo_cls = SommeRProcessData



    