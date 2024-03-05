import os

AFDB_URI = os.getenv("AFDB_URL")

UNIVERSAL_UNKNOWN = "NA"

ANALYZE_IMPLEMENTATIONS = {
    "asreml": "af.pipeline.asreml.analyze.AsremlAnalyze",
    "asreml-r": "af.pipeline.asreml_r.analyze.AsremlRAnalyze",
    "sommer": "af.pipeline.sommer.analyze.SommeRAnalyze",
    "sommer-mmec": "af.pipeline.sommer.analyze.SommeRAnalyze",
    "R - sommer-mmec": "af.pipeline.sommer.analyze.SommeRAnalyze",
}


def get_afdb_uri():
    return os.getenv("AFDB_URL")


def get_analysis_engine_script(engine_name: str):
    # This needs to configured from db
    engine = engine_name.lower()

    # Or this can just be defined by their respective Analyze classes
    if engine == "asreml":
        return "asreml"

    if engine in ["asremlr", "asreml-r", "asreml_r"]:
        return "asreml-r"

    if engine in ["r - sommer", "sommer"]:
        return "sommer"
    
    if engine in ["r - sommer mmec", "sommer mmec", "sommer-mmec"]:
        return "sommer-mmec"

    return None


def get_analyze_class(engine_name):
    """Gets the configured analyze class"""
    #
    kls = ANALYZE_IMPLEMENTATIONS.get(engine_name.lower())
    parts = kls.split(".")
    module = ".".join(parts[:-1])
    m = __import__(module)
    for comp in parts[1:]:
        m = getattr(m, comp)
    return m
