--liquibase formatted sql

--changeset postgres:Add_request_entry_table context:schema splitStatements:false rollbackSplitStatements:false
--comment: Add_request_entry_table




ALTER TABLE af.request_parameter 
 ALTER COLUMN value TYPE varchar(100);

CREATE TABLE af.request_entry
(
	experiment_id integer NOT NULL,
	entry_id integer NULL,
	tenant_id integer NULL,
	creation_timestamp timestamp without time zone NULL,
	modification_timestamp timestamp without time zone NULL,
	creator_id varchar(50) NULL,
	modifier_id varchar(50) NULL,
	is_void boolean NOT NULL   DEFAULT false,
	id integer NOT NULL DEFAULT NEXTVAL(('af."request_entry_id_seq"'::text)::regclass),
	request_id integer NOT NULL
)
;

CREATE SEQUENCE af.request_entry_id_seq INCREMENT 1 START 1;

ALTER TABLE af.request_entry ADD CONSTRAINT "PK_request_entry"
	PRIMARY KEY (id)
;

ALTER TABLE af.request_entry ADD CONSTRAINT "FK_request_entry_request"
	FOREIGN KEY (request_id) REFERENCES af.request (id) ON DELETE No Action ON UPDATE No Action
;