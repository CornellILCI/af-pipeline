#!/bin/sh

# Activate asreml license
asreml -z $ASREML_ACTIVATION_CODE

celery -A af.orchestrator.app worker --pool=gevent --concurrency=20 -l debug
