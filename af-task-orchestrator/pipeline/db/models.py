from sqlalchemy import Column, Integer, String, DateTime, Boolean, ForeignKey
from sqlalchemy.orm import relationship
from pipeline.db.core import Base


class Analysis(Base):

    __tablename__ = 'analysis'

    id = Column(Integer, primary_key=True)
    request_id = Column(String)
    sha = Column(String)
    request_type = Column(String)
    time_submitted = Column(DateTime)
    status = Column(String)
    msg = Column(String)


class Job(Base):

    __tablename__ = 'job'

    id = Column(Integer, primary_key=True)
    analysis_id = Column(Integer)
    name = Column(String)
    time_start = Column(DateTime)
    time_end = Column(DateTime)
    parent_id = Column(Integer)
    status = Column(Integer)
    err_msg = Column(String)


class Property(Base):

    __tablename__ = "property"  # Base.metadata.tables["af.property"]
    __table_args__ = {"schema": "af"}

    id = Column(Integer, primary_key=True)
    code = Column(String(50))
    name = Column(String(70))
    label = Column(String(70))
    description = Column(String(50))
    type = Column(String(50))
    data_type = Column(String(50))
    creation_timestamp = Column(DateTime)
    modification_timestamp = Column(DateTime)
    creator_id = Column(String(50))
    modifier_id = Column(String(50))
    is_void = Column(Boolean, default=False)
    tenant_id = Column(Integer)
    


class PropertyMeta(Base):
    __tablename__ = "property_meta"  # Base.metadata.tables["af.property_meta"]
    __table_args__ = {"schema": "af"}

    id = Column(Integer, primary_key=True)
    code = Column(String(50))
    creation_timestamp = Column(String(50))
    tenant_id = Column(Integer)
    creation_timestamp = Column(DateTime)
    modification_timestamp = Column(DateTime)
    creator_id = Column(String(50))
    modifier_id = Column(String(50))
    is_void = Column(Boolean, default=False)
    property_id = Column(Integer, primary_key=True)



class PropertyConfig(Base):
    __tablename__ = "property_config"  # Base.metadata.tables["af.request"]
    __table_args__ = {"schema": "af"}
    
    id = Column(Integer, primary_key=True)

    is_required = Column(Boolean, default=False)
    order_number = Column(Integer)

    creation_timestamp = Column(DateTime)
    modification_timestamp = Column(DateTime)
    creator_id = Column(String(50))
    modifier_id = Column(String(50))

    is_void = Column(Boolean, default=False)
    tenant_id = Column(Integer)

    property_id = Column(Integer, ForeignKey('af.property.id'))
    property_ui_id = Column(Integer,)

    config_property_id = Column(Integer)
    is_layout_variable =  Column(Boolean, default=False)


