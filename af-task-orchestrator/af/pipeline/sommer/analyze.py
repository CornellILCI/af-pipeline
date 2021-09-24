from af.pipeline.analyze import Analyze

from .dpo import SommeRProcessData


class SommeRAnalyze(Analyze):

    dpo_cls = SommeRProcessData
