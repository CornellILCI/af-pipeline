--liquibase formatted sql

--changeset postgres:Create_task_table context:schema splitStatements:false rollbackSplitStatements:false
--comment: DB-282 Create_task_table


ALTER TABLE af.request 
 ADD COLUMN msg varchar(500) NULL;

 CREATE TABLE af.task
(
	name varchar(50) NULL,
	time_start timestamp without time zone NULL,
	time_end timestamp without time zone NULL,
	status varchar(50) NULL,
	err_msg varchar(500) NULL,
	processor varchar(50) NULL,
	tenant_id integer NOT NULL,	-- Id of the selected Tenant
	creation_timestamp timestamp without time zone NOT NULL   DEFAULT now(),	-- Timestamp when the record was added to the table
	modification_timestamp timestamp without time zone NULL,	-- Timestamp when the record was last modified
	creator_id integer NOT NULL,	-- ID of the user who added the record to the table
	modifier_id integer NULL,	-- ID of the user who last modified the record
	is_void boolean NOT NULL   DEFAULT false,	-- Indicator whether the record is deleted (true) or not (false)
	id integer NOT NULL   DEFAULT NEXTVAL(('af."task_id_seq"'::text)::regclass),
	request_id integer NULL,
	parent_id integer NULL
);

CREATE SEQUENCE af.task_id_seq INCREMENT 1 START 1;

ALTER TABLE af.task ADD CONSTRAINT "PK_task"
    PRIMARY KEY (id);

ALTER TABLE af.task ADD CONSTRAINT "FK_task_request"
	FOREIGN KEY (request_id) REFERENCES af.request (id) ON DELETE No Action ON UPDATE No Action;

ALTER TABLE af.task ADD CONSTRAINT "FK_task_task"
	FOREIGN KEY (parent_id) REFERENCES af.task (id) ON DELETE No Action ON UPDATE No Action;

--Revert Changes
--rollback DROP TABLE af.task;
--rollback ALTER TABLE af.request DROP COLUMN msg;
--rollback DROP SEQUENCE af.task_id_seq;