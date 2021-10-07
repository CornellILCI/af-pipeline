--liquibase formatted sql

--changeset postgres:create_prediction_effect_table context:schema splitStatements:false rollbackSplitStatements:false
--comment: BA-656 Create prediction_effect table


DROP TABLE IF EXISTS af.effect;

DROP TABLE IF EXISTS af.prediction;

DROP TABLE IF EXISTS af.job_stat_factor;

DROP SEQUENCE IF EXISTS af.effect_id_seq;

DROP SEQUENCE IF EXISTS af.job_stat_factor_id_seq;

DROP SEQUENCE IF EXISTS af.prediction_id_seq;

CREATE TABLE af.prediction_effect
(
	id integer NOT NULL   DEFAULT NEXTVAL(('af."prediction_effect_id_seq"'::text)::regclass),
	job_id integer NOT NULL,
	factor jsonb NOT NULL,
	value decimal NULL,
	std_error decimal NULL,
	e_code text NULL,
	effect decimal NOT NULL,
	se_effect decimal NOT NULL,
	additional_info jsonb NULL,
	tenant_id integer NULL,	-- Id of the selected Tenant
	creation_timestamp timestamp without time zone NOT NULL   DEFAULT now(),	-- Timestamp when the record was added to the table
	modification_timestamp timestamp without time zone NULL,	-- Timestamp when the record was last modified
	creator_id integer NOT NULL,	-- ID of the user who added the record to the table
	modifier_id integer NULL,	-- ID of the user who last modified the record
	is_void boolean NOT NULL   DEFAULT false	-- Indicator whether the record is deleted (true) or not (false)
)
;

CREATE SEQUENCE af.prediction_effect_id_seq INCREMENT 1 START 1;

ALTER TABLE af.prediction_effect ADD CONSTRAINT "PK_prediction_effect"
	PRIMARY KEY (id)
;

ALTER TABLE af.prediction_effect ADD CONSTRAINT "FK_prediction_effect_job"
	FOREIGN KEY (job_id) REFERENCES af.job (id) ON DELETE No Action ON UPDATE No Action
;

COMMENT ON COLUMN af.prediction_effect.creation_timestamp
	IS 'Timestamp when the record was added to the table'
;

COMMENT ON COLUMN af.prediction_effect.creator_id
	IS 'ID of the user who added the record to the table'
;

COMMENT ON COLUMN af.prediction_effect.is_void
	IS 'Indicator whether the record is deleted (true) or not (false)'
;

COMMENT ON COLUMN af.prediction_effect.modification_timestamp
	IS 'Timestamp when the record was last modified'
;

COMMENT ON COLUMN af.prediction_effect.modifier_id
	IS 'ID of the user who last modified the record'


--Revert Changes

--rollback DROP TABLE af.prediction_effect;
--rollback DROP SEQUENCE af.prediction_effect_id_seq;

--rollback CREATE TABLE af.job_stat_factor (
--rollback 	factor_level int4 NULL,
--rollback 	tenant_id int4 NOT NULL,
--rollback 	creation_timestamp timestamp NOT NULL DEFAULT now(),
--rollback 	modification_timestamp timestamp NULL,
--rollback 	creator_id text NOT NULL,
--rollback 	modifier_id text NULL,
--rollback 	is_void bool NOT NULL DEFAULT false,
--rollback 	id serial NOT NULL,
--rollback 	job_id int4 NULL,
--rollback 	stat_factor int4 NULL,
--rollback 	CONSTRAINT "PK_job_stat_factor" PRIMARY KEY (id)
--rollback );

--rollback ALTER TABLE af.job_stat_factor ADD CONSTRAINT "FK_job_stat_factor_job" FOREIGN KEY (job_id) REFERENCES af.job(id);
--rollback ALTER TABLE af.job_stat_factor ADD CONSTRAINT "FK_job_stat_factor_property" FOREIGN KEY (stat_factor) REFERENCES af.property(id);

--rollback CREATE TABLE af.effect (
--rollback 	value float8 NULL,
--rollback 	se float8 NULL,
--rollback 	"type" text NULL,
--rollback 	gi float8 NULL,
--rollback 	aomstat float8 NULL,
--rollback 	amostat_flag text NULL,
--rollback 	tenant_id int4 NOT NULL,
--rollback 	creation_timestamp timestamp NOT NULL DEFAULT now(),
--rollback 	modification_timestamp timestamp NULL,
--rollback 	creator_id text NOT NULL,
--rollback 	modifier_id text NULL,
--rollback 	is_void bool NOT NULL DEFAULT false,
--rollback 	id serial NOT NULL,
--rollback 	job_stat_factor_id int4 NULL,
--rollback 	CONSTRAINT "PK_effect" PRIMARY KEY (id)
--rollback );

--rollback ALTER TABLE af.effect ADD CONSTRAINT "FK_effect_job_stat_factor" FOREIGN KEY (job_stat_factor_id) REFERENCES af.job_stat_factor(id);

--rollback CREATE TABLE af.prediction (
--rollback 	value float8 NULL,
--rollback 	std_error float8 NULL,
--rollback 	e_code text NULL,
--rollback 	tenant_id int4 NOT NULL,
--rollback 	creation_timestamp timestamp NOT NULL DEFAULT now(),
--rollback 	modification_timestamp timestamp NULL,
--rollback 	creator_id text NOT NULL,
--rollback 	modifier_id text NULL,
--rollback 	is_void bool NOT NULL DEFAULT false,
--rollback 	id serial NOT NULL,
--rollback 	job_stat_factor_id int4 NULL,
--rollback 	CONSTRAINT "PK_prediction" PRIMARY KEY (id)
--rollback );

--rollback ALTER TABLE af.prediction ADD CONSTRAINT "FK_prediction_job_stat_factor" FOREIGN KEY (job_stat_factor_id) REFERENCES af.job_stat_factor(id);