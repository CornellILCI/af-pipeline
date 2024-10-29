import os

# basic configs
broker_url = os.getenv("BROKER")
result_backend = os.getenv("BACKEND")

broker_heartbeat = 9000.0
broker_heartbeat_checkrate = 3

imports = "af.orchestrator.processing.analyze.asreml_tasks"
