import os

from af.pipeline.db.core import Base
from sqlalchemy import Boolean, Column, DateTime, Float, ForeignKey, Integer, String
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func


# workaround to get pytest to work with sqlite
if os.getenv("env") == "testing":
    from sqlalchemy import Float as DOUBLE_PRECISION
    from sqlalchemy.types import JSON
else:
    from sqlalchemy.dialects.postgresql import DOUBLE_PRECISION
    from sqlalchemy.dialects.postgresql import JSONB as JSON


class Request(Base):
    id: int
    uuid: str
    status: str
    tasks: list

    __tablename__ = "request"  # Base.metadata.tables["af.request"]
    __table_args__ = {"schema": "af"}

    uuid = Column(String)
    category = Column(String)
    type = Column(String)
    design = Column(String)
    requestor_id = Column(String)
    institute = Column(String)
    crop = Column(String)
    program = Column(String)
    status = Column(String)
    creation_timestamp = Column(DateTime)
    modification_timestamp = Column(DateTime)
    creator_id = Column(String)
    modifier_id = Column(String)
    is_void = Column(Boolean, default=False)
    tenant_id = Column(Integer)
    id = Column(Integer, primary_key=True)
    method_id = Column(Integer)
    engine = Column(String)
    msg = Column(String)

    # TODO add the other columns here
    tasks = relationship("Task", backref="request")


class Task(Base):
    __tablename__ = "task"
    __table_args__ = {"schema": "af"}

    name = Column(String)
    time_start = Column(DateTime)
    time_end = Column(DateTime)
    status = Column(String)
    err_msg = Column(String)
    processor = Column(String)
    tenant_id = Column(Integer, nullable=False)
    creation_timestamp = Column(DateTime, server_default=func.now())
    modification_timestamp = Column(DateTime)
    creator_id = Column(Integer, nullable=False)
    modifier_id = Column(Integer)
    is_void = Column(Boolean, nullable=False, default=False)
    id = Column(Integer, primary_key=True)
    request_id = Column(Integer, ForeignKey("af.request.id"))
    parent_id = Column(Integer)


class Analysis(Base):

    __tablename__ = "analysis"
    __table_args__ = {"schema": "af"}

    id = Column(Integer, primary_key=True)
    name = Column(String)
    description = Column(String)
    request_id = Column(Integer)
    prediction_id = Column(Integer)
    creation_timestamp = Column(DateTime)
    modification_timestamp = Column(DateTime)
    creator_id = Column(String)
    modifier_id = Column(String)
    status = Column(String)
    is_void = Column(Boolean, default=False)
    tenant_id = Column(Integer)
    model_id = Column(Integer)


class Job(Base):

    __tablename__ = "job"
    __table_args__ = {"schema": "af"}

    id = Column(Integer, primary_key=True)
    analysis_id = Column(Integer)
    name = Column(String)
    time_start = Column(DateTime)
    time_end = Column(DateTime)
    output_path = Column(String)
    creation_timestamp = Column(DateTime)
    modification_timestamp = Column(DateTime)
    creator_id = Column(String)
    modifier_id = Column(String)
    status = Column(String)
    status_message = Column(String)
    is_void = Column(Boolean, default=False)
    tenant_id = Column(Integer)


class Property(Base):

    __tablename__ = "property"
    __table_args__ = {"schema": "af"}

    id = Column(Integer, primary_key=True)
    code = Column(String)
    name = Column(String)
    label = Column(String)
    description = Column(String)
    type = Column(String)
    data_type = Column(String)
    creation_timestamp = Column(DateTime)
    modification_timestamp = Column(DateTime)
    creator_id = Column(String)
    modifier_id = Column(String)
    is_void = Column(Boolean, default=False)
    tenant_id = Column(Integer)
    statement = Column(String)


class PropertyMeta(Base):
    __tablename__ = "property_meta"
    __table_args__ = {"schema": "af"}

    id = Column(Integer, primary_key=True)
    code = Column(String)
    value = Column(String)
    tenant_id = Column(Integer)
    creation_timestamp = Column(DateTime)
    modification_timestamp = Column(DateTime)
    creator_id = Column(String)
    modifier_id = Column(String)
    is_void = Column(Boolean, default=False)
    property_id = Column(Integer)


class PropertyConfig(Base):
    __tablename__ = "property_config"
    __table_args__ = {"schema": "af"}

    id = Column(Integer, primary_key=True)

    is_required = Column(Boolean, default=False)
    order_number = Column(Integer)

    creation_timestamp = Column(DateTime)
    modification_timestamp = Column(DateTime)
    creator_id = Column(String)
    modifier_id = Column(String)

    is_void = Column(Boolean, default=False)
    tenant_id = Column(Integer)

    property_id = Column(Integer, ForeignKey("af.property.id"))
    property_ui_id = Column(
        Integer,
    )

    config_property_id = Column(Integer)
    is_layout_variable = Column(Boolean, default=False)


class Variance(Base):
    __tablename__ = "variance"
    __table_args__ = {"schema": "af"}

    id = Column(Integer, primary_key=True)

    source = Column(String)  # character varying(50) COLLATE pg_catalog."default",
    model = Column(String)  # character varying(50) COLLATE pg_catalog."default",
    gamma = Column(DOUBLE_PRECISION)  # double precision,
    component = Column(DOUBLE_PRECISION)  # double precision,
    component_ratio = Column(DOUBLE_PRECISION)  # double precision,
    last_change_percentage = Column(DOUBLE_PRECISION)  # double precision,
    code = Column(String)  # character varying(50) COLLATE pg_catalog."default",
    tenant_id = Column(Integer, nullable=False)  # integer NOT NULL,
    creation_timestamp = Column(DateTime)  # timestamp without time zone NOT NULL DEFAULT now(),
    modification_timestamp = Column(DateTime)  # timestamp without time zone,
    creator_id = Column(Integer, nullable=False)  # integer NOT NULL,
    modifier_id = Column(Integer)
    is_void = Column(Boolean, nullable=False, default=False)
    job_id = Column(Integer)


class ModelStat(Base):
    __tablename__ = "model_stat"
    __table_args__ = {"schema": "af"}

    id = Column(Integer, primary_key=True)

    log_lik = Column(DOUBLE_PRECISION)  # double precision,
    aic = Column(DOUBLE_PRECISION)  # double precision,
    bic = Column(DOUBLE_PRECISION)  # double precision,
    components = Column(Integer)  # integer,
    tenant_id = Column(Integer, nullable=False)
    creation_timestamp = Column(DateTime)  # timestamp without time zone NOT NULL DEFAULT now(),
    modification_timestamp = Column(DateTime)  # timestamp without time zone,
    creator_id = Column(Integer, nullable=False)
    modifier_id = Column(Integer)
    is_void = Column(Boolean, nullable=False, default=False)
    job_id = Column(Integer)
    conclusion = Column(String(500))
    is_converged = Column(Boolean, default=False)


class Prediction(Base):
    __tablename__ = "prediction"
    __table_args__ = {"schema": "af"}

    id = Column(Integer, primary_key=True)

    value = Column(Float)
    std_error = Column(Float)
    e_code = Column(String)
    ci95_upper = Column(Float)
    ci95_lower = Column(Float)
    tenant_id = Column(Integer, nullable=False)
    creation_timestamp = Column(DateTime)  # timestamp without time zone NOT NULL DEFAULT now(),
    modification_timestamp = Column(DateTime)  # timestamp without time zone,
    creator_id = Column(Integer, nullable=False)
    modifier_id = Column(Integer)
    is_void = Column(Boolean, nullable=False, default=False)
    job_stat_factor_id = Column(Integer)

    additional_info = Column(JSON, nullable=True)


class FittedValues(Base):
    __tablename__ = "fitted_values"
    __table_args__ = {"schema": "af"}

    id = Column(Integer, primary_key=True)

    record = Column(Integer)
    trait_value = Column(DOUBLE_PRECISION)
    yhat = Column(DOUBLE_PRECISION)
    residual = Column(DOUBLE_PRECISION)
    hat = Column(DOUBLE_PRECISION)
    plot_id = Column(Integer)
    stat_factor = Column(String)
    tenant_id = Column(Integer, nullable=False)
    creation_timestamp = Column(DateTime, server_default=func.now())
    modification_timestamp = Column(DateTime)
    creator_id = Column(Integer, nullable=False)
    modifier_id = Column(Integer)
    is_void = Column(Boolean, nullable=False, default=False)
    
    job_id = Column(Integer)
    additional_info = Column(JSON, nullable=True)
    # TODO add ref to job
