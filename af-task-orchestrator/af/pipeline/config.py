import os

AFDB_URI = os.getenv("AFDB_URL")

UNIVERSAL_UNKNOWN = "NA"

#Why is this here? Why is it hiding? Why are we returning 'name' in one place then having a lookup table to the class impl, and why is it ALL STRINGLY TYPED 
# We could load the 'kls' once, attach it to some kind of object.... <trails off>
#   - Respectfully, JDLS
ANALYZE_IMPLEMENTATIONS = {
    "asreml": "af.pipeline.asreml.analyze.AsremlAnalyze",
    "asreml-r": "af.pipeline.asreml_r.analyze.AsremlRAnalyze",
    "sommer": "af.pipeline.sommer.analyze.SommeRAnalyze",
    "sommer-mmec": "af.pipeline.sommer.analyze-mmec.SommeRmmecAnalyze",
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
    
    if engine in ["r - sommer mmec", "sommer mmec", "sommer-mmec", "sommer - mmec"]:
        return "sommer-mmec"

    print(f"Invalid engine name: {engine}")#This is uaually a straight lookup, why this table in the first place?
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
