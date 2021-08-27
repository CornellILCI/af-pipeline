import os

AFDB_URI = os.getenv("AFDB_URL")

UNIVERSAL_UNKNOWN = "NA"

ANALYZE_IMPLEMENTATIONS = {
    "asreml": "af.pipeline.asreml.analyze.AsremlAnalyze",
    "sommer": "af.pipeline.sommer.analyze.SommerAnalyze"
}


def get_afdb_uri():
    return os.getenv("AFDB_URL")


def get_analysis_engine_script(engine_name: str):
    # This needs to configured from db
    engine = engine_name.lower()
    if engine == "asreml":
        return "asreml"
    
    if engine == "sommer":
        return "sommeR"


def get_analyze_class(engine_name):
    """Gets the configured analyze class"""
    # 
    kls = ANALYZE_IMPLEMENTATIONS.get(engine_name.lower())
    parts = kls.split('.')
    module = ".".join(parts[:-1])
    m = __import__(module)
    for comp in parts[1:]:
        m = getattr(m, comp)
    return m
