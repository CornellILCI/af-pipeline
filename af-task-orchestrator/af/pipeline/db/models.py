import os

from af.pipeline.db.core import Base
from sqlalchemy import Boolean, Column, DateTime, Float, ForeignKey, Integer, String, Numeric
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func

import datetime

# workaround to get pytest to work with sqlite
if os.getenv("env") == "testing":
    from sqlalchemy import Float as DOUBLE_PRECISION
    from sqlalchemy.types import JSON
else:
    from sqlalchemy.dialects.postgresql import DOUBLE_PRECISION
    from sqlalchemy.dialects.postgresql import JSONB as JSON


class BaseMixin(object):

    __table_args__ = {"schema": "af"}

    id = Column(Integer, primary_key=True)

    creation_timestamp = Column(DateTime, default=datetime.datetime.now())
    modification_timestamp = Column(DateTime, default=datetime.datetime.now())
    creator_id = Column(String)
    modifier_id = Column(String)
    is_void = Column(Boolean, default=False)


class Request(BaseMixin, Base):

    __tablename__ = "request"  # Base.metadata.tables["af.request"]

    uuid = Column(String)
    category = Column(String)
    type = Column(String)
    design = Column(String)
    requestor_id = Column(String)
    institute = Column(String)
    crop = Column(String)
    program = Column(String)
    tenant_id = Column(Integer)
    method_id = Column(Integer)

    engine = Column(String)

    status = Column(String)
    msg = Column(String)

    # TODO add the other columns here
    tasks = relationship("Task", backref="request")


class Task(BaseMixin, Base):

    __tablename__ = "task"

    name = Column(String)
    time_start = Column(DateTime)
    time_end = Column(DateTime)
    status = Column(String)
    err_msg = Column(String)
    processor = Column(String)
    tenant_id = Column(Integer, nullable=False)
    request_id = Column(Integer, ForeignKey("af.request.id"))
    parent_id = Column(Integer)


class Analysis(BaseMixin, Base):

    __tablename__ = "analysis"

    name = Column(String)
    description = Column(String)
    request_id = Column(Integer)
    prediction_id = Column(Integer)
    status = Column(String)
    tenant_id = Column(Integer)
    model_id = Column(Integer)
    
    jobs = relationship("Job", back_populates="analysis")  


class Job(BaseMixin, Base):

    __tablename__ = "job"

    analysis_id = Column(Integer, ForeignKey(Analysis.id))
    name = Column(String)
    time_start = Column(DateTime)
    time_end = Column(DateTime)
    output_path = Column(String)
    status = Column(String)
    status_message = Column(String)
    tenant_id = Column(Integer)

    analysis = relationship(Analysis, back_populates="jobs") 


class Property(BaseMixin, Base):

    __tablename__ = "property"

    code = Column(String)
    name = Column(String)
    label = Column(String)
    description = Column(String)
    type = Column(String)
    data_type = Column(String)
    tenant_id = Column(Integer)
    statement = Column(String)


class PropertyMeta(BaseMixin, Base):

    __tablename__ = "property_meta"

    code = Column(String)
    value = Column(String)
    tenant_id = Column(Integer)
    property_id = Column(Integer)


class PropertyConfig(BaseMixin, Base):

    __tablename__ = "property_config"

    is_required = Column(Boolean, default=False)
    order_number = Column(Integer)

    tenant_id = Column(Integer)

    property_id = Column(Integer, ForeignKey("af.property.id"))
    property_ui_id = Column(
        Integer,
    )

    config_property_id = Column(Integer)
    is_layout_variable = Column(Boolean, default=False)


class Variance(BaseMixin, Base):

    __tablename__ = "variance"

    source = Column(String)  # character varying(50) COLLATE pg_catalog."default",
    model = Column(String)  # character varying(50) COLLATE pg_catalog."default",
    gamma = Column(DOUBLE_PRECISION)  # double precision,
    component = Column(DOUBLE_PRECISION)  # double precision,
    component_ratio = Column(DOUBLE_PRECISION)  # double precision,
    last_change_percentage = Column(DOUBLE_PRECISION)  # double precision,
    code = Column(String)  # character varying(50) COLLATE pg_catalog."default",
    tenant_id = Column(Integer, nullable=False)  # integer NOT NULL,

    job_id = Column(Integer)


class ModelStat(BaseMixin, Base):

    __tablename__ = "model_stat"

    log_lik = Column(DOUBLE_PRECISION)  # double precision,
    aic = Column(DOUBLE_PRECISION)  # double precision,
    bic = Column(DOUBLE_PRECISION)  # double precision,
    components = Column(Integer)  # integer,
    tenant_id = Column(Integer, nullable=False)
    job_id = Column(Integer)
    conclusion = Column(String(500))
    is_converged = Column(Boolean, default=False)


class PredictionEffect(BaseMixin, Base):

    __tablename__ = "prediction_effect"

    value = Column(Float)
    
    std_error = Column(Float)
    e_code = Column(String)

    factor = Column(JSON)

    effect = Column(Numeric, default=0)
    se_effect = Column(Numeric, default=0)

    tenant_id = Column(Integer, nullable=False)
    
    is_void = Column(Boolean, nullable=False, default=False)

    additional_info = Column(JSON, nullable=True)


class FittedValues(BaseMixin, Base):

    __tablename__ = "fitted_values"

    record = Column(Integer)
    trait_value = Column(DOUBLE_PRECISION)
    yhat = Column(DOUBLE_PRECISION)
    residual = Column(DOUBLE_PRECISION)
    hat = Column(DOUBLE_PRECISION)
    plot_id = Column(Integer)
    stat_factor = Column(String)
    tenant_id = Column(Integer, nullable=False)

    job_id = Column(Integer)
    additional_info = Column(JSON, nullable=True)
    # TODO add ref to job
