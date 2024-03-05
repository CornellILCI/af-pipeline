from __future__ import annotations

from dataclasses import dataclass

from database import Property, db
from sqlalchemy.sql import func


# @dataclass
# class Request(db.Model):
#     __tablename__ = "request"  # Base.metadata.tables["af.request"]

#     uuid = db.Column(db.String)
#     category = db.Column(db.String)
#     type = db.Column(db.String)
#     design = db.Column(db.String)
#     requestor_id = db.Column(db.String)
#     institute = db.Column(db.String)
#     crop = db.Column(db.String)
#     program = db.Column(db.String)
#     method_id = db.Column(db.Integer)
#     engine = db.Column(db.String)
#     msg = db.Column(db.String)
#     status = db.Column(db.String)

#     # TODO add the other columns here
#     tasks = db.relationship("Task", backref="request", foreign_keys="Task.request_id")

#     analyses = db.relationship("Analysis", back_populates="request")


# @dataclass
# class AnalysisConfig(db.Model):

#     __tablename__ = "property"

#     code = db.Column(db.String)
#     name = db.Column(db.String)
#     description: db.Column(db.String)

#     prediction_id = db.Column(db.Integer, db.ForeignKey(Property.id))
#     model_id = db.Column(db.Integer, db.ForeignKey(Property.id))

#     request = db.relationship(Request, back_populates="analyses")
#     jobs = db.relationship("Job", back_populates="analysis")

#     # map for all relationships to Property
#     prediction = db.relationship(Property, foreign_keys=[prediction_id])
#     analysis_objective = db.relationship(Property, foreign_keys=[analysis_objective_id])


# @dataclass
# class AnalysisConfigMeta(db.Model):

#     __tablename__ = "property_meta"

#     config_id = db.Column(db.String)
#     config_version = db.Column(db.String)
#     created_on = db.Column(db.String)
#     author = db.Column(db.String)
#     email = db.Column(db.String)
#     engine = db.Column(db.String)
#     experiment_info = db.Column(db.String)
#     breeding_program_id = db.Column(db.String)
#     pipeline_id = db.Column(db.String)
#     stage_id = db.Column(db.String)
#     design = db.Column(db.String)
#     trait_level = db.Column(db.String)
#     analysis_info = db.Column(db.String)
#     analysis_objective = db.Column(db.String)
#     exp_analysis_pattern = db.Column(db.String)
#     loc_analysis_pattern = db.Column(db.String)
#     year_analysis_pattern = db.Column(db.String)
#     trait_pattern = db.Column(db.String)

#     prediction_id = db.Column(db.Integer, db.ForeignKey(Property.id))
#     model_id = db.Column(db.Integer, db.ForeignKey(Property.id))

#     request = db.relationship(Request, back_populates="analyses")
#     jobs = db.relationship("Job", back_populates="analysis")

