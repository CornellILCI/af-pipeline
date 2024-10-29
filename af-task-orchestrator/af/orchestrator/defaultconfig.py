import os

# basic configs
broker_url = os.getenv("BROKER")
result_backend = os.getenv("BACKEND")

broker_heartbeat=9000.0
broker_heartbeat_checkrate=3

#Disable 'heartbeat' as long sommer tasks 'hang' the worker, which is detected as a dead worker and is killed
#broker_heartbeat = 0

imports = ["af.orchestrator.processing.analyze.tasks", "af.orchestrator.processing.analyze.sommer_tasks"]
