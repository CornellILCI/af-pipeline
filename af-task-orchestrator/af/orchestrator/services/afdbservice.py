import datetime

from af.orchestrator.db.models import Request, Task
from af.pipeline.db.core import DBConfig


class AFDBService:
    def __init__(self, _session=None):
        self._session = _session or DBConfig.get_session()

    def get_af_request(self, request_uuid):
        return self._session.query(Request).filter_by(uuid=request_uuid).first()

    def create_request_task_entry(self, request: Request, name):
        task = Task(
            name=name,
            time_start=datetime.datetime.now(),
            status="STARTED",
            processor="celery",
            tenant_id=1,
            creator_id=1,
        )
        request.tasks.append(task)
        self._session.merge(request)
        self._session.commit()
        return task

    def update_task_status(self, task: Task, status):
        task.status = status
        task.time_end = datetime.datetime.now()
        self._session.merge(task)
        self._session.commit()

    def update_request_status(self, request: Request, status):
        request.status = status
        self._session.merge(request)
        self._session.commit()

    def remove_session(self):
        self._session.remove()
