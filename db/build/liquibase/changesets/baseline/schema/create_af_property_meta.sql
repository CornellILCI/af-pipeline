-- Deploy analyticalframework: to pg

--liquibase formatted sql

--changeset postgres:create_af_property_meta context:schema splitStatements:false rollbackSplitStatements:false
--comment: create_af_property_meta



CREATE TABLE af.property_meta
(
	id integer NOT NULL   DEFAULT NEXTVAL(('af."property_meta_id_seq"'::text)::regclass),
    code varchar(20) NOT NULL,
	value varchar(255) NOT NULL,
	tenant_id integer NULL,
	creation_timestamp timestamp without time zone NULL,
	modification_timestamp timestamp without time zone NULL,
	creator_id varchar(50) NULL,
	modifier_id varchar(50) NULL,
	is_void boolean NULL,
	property_id integer NOT NULL
)
;

CREATE SEQUENCE af.property_meta_id_seq INCREMENT 1 START 1;


ALTER TABLE af.property_meta ADD CONSTRAINT "PK_property_meta"
	PRIMARY KEY (id)
;

ALTER TABLE af.property_meta ADD CONSTRAINT "FK_property_meta_property"
	FOREIGN KEY (property_id) REFERENCES af.property (id) ON DELETE No Action ON UPDATE No Action
;

ALTER TABLE af.request 
 ALTER COLUMN category TYPE varchar(50);

ALTER TABLE af.request 
 ALTER COLUMN requestor_id TYPE varchar(50);

ALTER TABLE af.request 
 ADD COLUMN engine varchar(20) NULL;