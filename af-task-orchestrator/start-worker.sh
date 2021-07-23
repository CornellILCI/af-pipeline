#!/bin/sh

# Activate asreml license
echo $ASREML_ACTIVATION_CODE
asreml -z $ASREML_ACTIVATION_CODE


celery multi start default ASREML -c:default 10 -c:ASREML ${ASREML_SEATS:-1}  -Q:default default -Q:ASREML ASREML -A af.orchestrator.app worker  -l $LOG_LEVEL
