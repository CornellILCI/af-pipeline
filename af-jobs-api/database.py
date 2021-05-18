
import datetime
from dataclasses import dataclass
from sqlalchemy.sql import func

from flask_sqlalchemy import SQLAlchemy, SignallingSession, SessionBase


class _SignallingSession(SignallingSession):
    """A subclass of `SignallingSession` that allows for `binds` to be specified
    in the `options` keyword arguments.
    """
    def __init__(self, db, autocommit=False, autoflush=True, **options):
        self.app = db.get_app()
        self._model_changes = {}
        self.emit_modification_signals = \
            self.app.config['SQLALCHEMY_TRACK_MODIFICATIONS']

        bind = options.pop('bind', None)
        if bind is None:
            bind = db.engine

        binds = options.pop('binds', None)
        if binds is None:
            binds = db.get_binds(self.app)

        SessionBase.__init__(self,
                             autocommit=autocommit,
                             autoflush=autoflush,
                             bind=bind,
                             binds=binds,
                             **options)


class _SQLAlchemy(SQLAlchemy):
    """A subclass of `SQLAlchemy` that uses `_SignallingSession`."""
    def create_session(self, options):
        return _SignallingSession(self, **options)


db = _SQLAlchemy()

#database instance
#db = SQLAlchemy()

# models
@dataclass
class Request(db.Model):
    id: int
    uuid: str
    status: str
    tasks: list

    __tablename__ = "request"  # Base.metadata.tables["af.request"]
    __table_args__ = {"schema": "af"}

    uuid = db.Column(db.String(50))
    category = db.Column(db.String(50))
    type = db.Column(db.String(50))
    design = db.Column(db.String(50))
    requestor_id = db.Column(db.String(50))
    institute = db.Column(db.String(50))
    crop = db.Column(db.String(50))
    program = db.Column(db.String(50))
    status = db.Column(db.String(50))
    creation_timestamp = db.Column(db.DateTime, server_default=func.now())
    modification_timestamp = db.Column(db.DateTime)
    creator_id = db.Column(db.String(50))
    modifier_id = db.Column(db.String(50))
    is_void = db.Column(db.Boolean, default=False)
    tenant_id = db.Column(db.Integer)
    id = db.Column(db.Integer, primary_key=True)
    method_id = db.Column(db.Integer)
    engine = db.Column(db.String(20))
    msg = db.Column(db.String(500))

    # TODO add the other columns here
    tasks = db.relationship("Task", backref="request", foreign_keys="Task.request_id")


@dataclass
class Task(db.Model):
    id: int
    name: str
    time_start: datetime.datetime
    time_end: datetime.datetime
    status: str
    err_msg: str
    processor: str
    request_id: int

    __tablename__ = "task"
    __table_args__ = {"schema": "af"}

    name = db.Column(db.String(50))
    time_start = db.Column(db.DateTime)
    time_end = db.Column(db.DateTime)
    status = db.Column(db.String(50))
    err_msg = db.Column(db.String(500))
    processor = db.Column(db.String(50))
    tenant_id = db.Column(db.Integer, nullable=False)
    creation_timestamp = db.Column(db.DateTime, server_default=func.now())
    modification_timestamp = db.Column(db.DateTime)
    creator_id = db.Column(db.Integer, nullable=False)
    modifier_id = db.Column(db.Integer)
    is_void = db.Column(db.Boolean, nullable=False, default=False)
    id = db.Column(db.Integer, primary_key=True)
    request_id = db.Column(db.Integer, db.ForeignKey("af.request.id"))
    parent_id = db.Column(db.Integer)
