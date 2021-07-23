#!/bin/sh

# Activate asreml license
asreml -z $ASREML_ACTIVATION_CODE

celery multi start default ASREML -c:default 10 -c:ASREML ${ASREML_SEATS:-1} -A af.orchestrator.app worker  -l $LOG_LEVEL
