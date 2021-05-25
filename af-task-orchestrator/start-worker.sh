#!/bin/sh
celery -A orchestrator.app worker --pool=gevent --concurrency=20 -l debug