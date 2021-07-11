#!/bin/sh
CONC="${ASREML_LICENSE_SEATS:-1}"
echo "Starting ASREML worker with ${CONC} processes"
celery -A af.orchestrator.app worker --pool=gevent --concurrency=$CONC -Q ASREML 