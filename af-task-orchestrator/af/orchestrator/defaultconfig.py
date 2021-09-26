import os

# basic configs
broker_url = os.getenv("BROKER")
result_backend = os.getenv("BACKEND")

imports = "af.orchestrator.processing.analyze.tasks"
