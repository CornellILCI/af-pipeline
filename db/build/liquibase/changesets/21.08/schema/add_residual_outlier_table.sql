--liquibase formatted sql

--changeset postgres:add_residual_outlier_table context:schema splitStatements:false rollbackSplitStatements:false
--comment: BA-639 Add residual_outlier table


CREATE TABLE af.residual_outlier
(
	id integer NOT NULL   DEFAULT NEXTVAL(('af."residual_outlier_id_seq"'::text)::regclass),
	outlier jsonb NULL,
	job_id integer NOT NULL,
	tenant_id integer NOT NULL,	-- Id of the selected Tenant
	creation_timestamp timestamp without time zone NOT NULL   DEFAULT now(),	-- Timestamp when the record was added to the table
	modification_timestamp timestamp without time zone NULL,	-- Timestamp when the record was last modified
	creator_id integer NOT NULL,	-- ID of the user who added the record to the table
	modifier_id integer NULL,	-- ID of the user who last modified the record
	is_void boolean NOT NULL   DEFAULT false	-- Indicator whether the record is deleted (true) or not (false)
)
;

CREATE SEQUENCE af.residual_outlier_id_seq INCREMENT 1 START 1;

ALTER TABLE af.residual_outlier ADD CONSTRAINT "PK_residual_outlier"
	PRIMARY KEY (id)
;

ALTER TABLE af.residual_outlier ADD CONSTRAINT "FK_residual_outlier_job"
	FOREIGN KEY (job_id) REFERENCES af.job (id) ON DELETE No Action ON UPDATE No Action
;

COMMENT ON COLUMN af.residual_outlier.creation_timestamp
	IS 'Timestamp when the record was added to the table'
;

COMMENT ON COLUMN af.residual_outlier.creator_id
	IS 'ID of the user who added the record to the table'
;

COMMENT ON COLUMN af.residual_outlier.is_void
	IS 'Indicator whether the record is deleted (true) or not (false)'
;

COMMENT ON COLUMN af.residual_outlier.modification_timestamp
	IS 'Timestamp when the record was last modified'
;

COMMENT ON COLUMN af.residual_outlier.modifier_id
	IS 'ID of the user who last modified the record'
;

COMMENT ON COLUMN af.residual_outlier.tenant_id
	IS 'Id of the selected Tenant'
;

--Revert Changes
--rollback DROP TABLE af.residual_outlier;
--rollback DROP SEQUENCE IF EXISTS af.residual_outlier_id_seq;