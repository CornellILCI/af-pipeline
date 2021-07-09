from __future__ import annotations

from dataclasses import dataclass

from database import db
from sqlalchemy.sql import func


@dataclass
class Request(db.Model):

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
