#!/bin/sh
celery -A af.orchestrator.app worker --pool=gevent --concurrency=20 -l debug