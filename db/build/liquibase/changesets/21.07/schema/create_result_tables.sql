--liquibase formatted sql

--changeset postgres:create_result_tables context:schema splitStatements:false rollbackSplitStatements:false
--comment: DB-370 Create results tables in badb

CREATE TABLE af.prediction
(
	id integer NOT NULL   DEFAULT NEXTVAL(('af."prediction_id_seq"'::text)::regclass),
	job_stat_factor_id integer NULL
	value text NULL,
	std_error text NULL,
	e_code text NULL,
	additional_info jsonb NULL, -- Any additional information related to prediction
	tenant_id integer NULL,	-- Id of the selected Tenant
	creation_timestamp timestamp without time zone NOT NULL DEFAULT now(),	-- Timestamp when the record was added to the table
	modification_timestamp timestamp without time zone NULL,	-- Timestamp when the record was last modified
	creator_id integer NOT NULL,	-- ID of the user who added the record to the table
	modifier_id integer NULL,	-- ID of the user who last modified the record
	is_void boolean NOT NULL DEFAULT false,	-- Indicator whether the record is deleted (true) or not (false)
)
;


CREATE TABLE af.fitted_values
(
	id integer NOT NULL   DEFAULT NEXTVAL(('af."fitted_values_id_seq"'::text)::regclass),
	job_id integer NOT NULL
	record integer NULL,
	yhat text NULL,
	residual text NULL,
	hat text NULL,
	plot_id integer NULL,
	additional_info jsonb NULL, -- Any additional information related to prediction
	stat_factor text NULL,
	tenant_id integer NULL,	-- Id of the selected Tenant
	creation_timestamp timestamp without time zone NOT NULL DEFAULT now(),	-- Timestamp when the record was added to the table
	modification_timestamp timestamp without time zone NULL, -- Timestamp when the record was last modified
	creator_id integer NOT NULL,	-- ID of the user who added the record to the table
	modifier_id integer NULL,	-- ID of the user who last modified the record
	is_void boolean NOT NULL   DEFAULT false,	-- Indicator whether the record is deleted (true) or not (false)
)
;


CREATE TABLE af.job_data
(
	id integer NOT NULL DEFAULT NEXTVAL(('af."job_data_id_seq"'::text)::regclass),
	job_id integer NULL,
	data varchar(50) NULL,
	value integer NULL,
	tenant_id integer NULL,	-- Id of the selected Tenant
	creation_timestamp timestamp without time zone NOT NULL DEFAULT now(),	-- Timestamp when the record was added to the table
	modification_timestamp timestamp without time zone NULL,	-- Timestamp when the record was last modified
	creator_id integer NOT NULL,	-- ID of the user who added the record to the table
	modifier_id integer NULL,	-- ID of the user who last modified the record
	is_void boolean NOT NULL   DEFAULT false,	-- Indicator whether the record is deleted (true) or not (false)
)
;

CREATE TABLE af.job_stat_factor
(
	id integer NOT NULL   DEFAULT NEXTVAL(('af."job_stat_factor_id_seq"'::text)::regclass),
	job_id integer NULL,
	stat_factor integer NULL,
	factor_level integer NULL,
	tenant_id integer NULL,	-- Id of the selected Tenant
	creation_timestamp timestamp without time zone NOT NULL DEFAULT now(),	-- Timestamp when the record was added to the table
	modification_timestamp timestamp without time zone NULL,	-- Timestamp when the record was last modified
	creator_id integer NOT NULL,	-- ID of the user who added the record to the table
	modifier_id integer NULL,	-- ID of the user who last modified the record
	is_void boolean NOT NULL   DEFAULT false,	-- Indicator whether the record is deleted (true) or not (false)
)
;

CREATE TABLE af.model_stat
(
	log_lik double precision NULL,
	aic double precision NULL,
	bic double precision NULL,
	components integer NULL,
	tenant_id integer NOT NULL,	-- Id of the selected Tenant
	creation_timestamp timestamp without time zone NOT NULL   DEFAULT now(),	-- Timestamp when the record was added to the table
	modification_timestamp timestamp without time zone NULL,	-- Timestamp when the record was last modified
	creator_id integer NOT NULL,	-- ID of the user who added the record to the table
	modifier_id integer NULL,	-- ID of the user who last modified the record
	is_void boolean NOT NULL   DEFAULT false,	-- Indicator whether the record is deleted (true) or not (false)
	id integer NOT NULL   DEFAULT NEXTVAL(('af."model_stat_id_seq"'::text)::regclass),
	job_id integer NULL
)
;


CREATE TABLE af.variance
(
	source varchar(50) NULL,
	model varchar(50) NULL,
	gamma double precision NULL,
	component double precision NULL,
	component_ratio double precision NULL,
	last_change_percentage double precision NULL,
	code varchar(50) NULL,
	tenant_id integer NOT NULL,	-- Id of the selected Tenant
	creation_timestamp timestamp without time zone NOT NULL   DEFAULT now(),	-- Timestamp when the record was added to the table
	modification_timestamp timestamp without time zone NULL,	-- Timestamp when the record was last modified
	creator_id integer NOT NULL,	-- ID of the user who added the record to the table
	modifier_id integer NULL,	-- ID of the user who last modified the record
	is_void boolean NOT NULL   DEFAULT false,	-- Indicator whether the record is deleted (true) or not (false)
	id integer NOT NULL   DEFAULT NEXTVAL(('af."variance_id_seq"'::text)::regclass),
	job_id integer NULL
)
;

CREATE TABLE af.effect
(
	value double precision NULL,
	se double precision NULL,
	type varchar(50) NULL,
	gi double precision NULL,
	aomstat double precision NULL,
	amostat_flag varchar(50) NULL,
	tenant_id integer NOT NULL,	-- Id of the selected Tenant
	creation_timestamp timestamp without time zone NOT NULL   DEFAULT now(),	-- Timestamp when the record was added to the table
	modification_timestamp timestamp without time zone NULL,	-- Timestamp when the record was last modified
	creator_id integer NOT NULL,	-- ID of the user who added the record to the table
	modifier_id integer NULL,	-- ID of the user who last modified the record
	is_void boolean NOT NULL   DEFAULT false,	-- Indicator whether the record is deleted (true) or not (false)
	id integer NOT NULL   DEFAULT NEXTVAL(('"af.effect_id_seq"'::text)::regclass),
	job_stat_factor_id integer NULL
)
;

CREATE SEQUENCE af.fitted_values_id_seq INCREMENT 1 START 1;

CREATE SEQUENCE af.job_data_id_seq INCREMENT 1 START 1;

CREATE SEQUENCE af.job_stat_factor_id_seq INCREMENT 1 START 1;

CREATE SEQUENCE af.model_stat_id_seq INCREMENT 1 START 1;

CREATE SEQUENCE af.prediction_id_seq INCREMENT 1 START 1;

CREATE SEQUENCE af.variance_id_seq INCREMENT 1 START 1;

CREATE SEQUENCE af.effect_id_seq INCREMENT 1 START 1;

ALTER TABLE af.fitted_values ADD CONSTRAINT "PK_fitted_values"
	PRIMARY KEY (id)
;

ALTER TABLE af.job_data ADD CONSTRAINT "PK_job_data"
	PRIMARY KEY (id)
;

ALTER TABLE af.job_stat_factor ADD CONSTRAINT "PK_job_stat_factor"
	PRIMARY KEY (id)
;

ALTER TABLE af.model_stat ADD CONSTRAINT "PK_model_stat"
	PRIMARY KEY (id)
;

ALTER TABLE af.prediction ADD CONSTRAINT "PK_prediction"
	PRIMARY KEY (id)
;

ALTER TABLE af.variance ADD CONSTRAINT "PK_variance"
	PRIMARY KEY (id)
;

ALTER TABLE af.effect ADD CONSTRAINT "PK_effect"
	PRIMARY KEY (id)
;

ALTER TABLE af.fitted_values ADD CONSTRAINT "FK_fitted_values_job"
	FOREIGN KEY (job_id) REFERENCES af.job (id) ON DELETE No Action ON UPDATE No Action
;

ALTER TABLE af.job_data ADD CONSTRAINT "FK_job_data_job"
	FOREIGN KEY (job_id) REFERENCES af.job (id) ON DELETE No Action ON UPDATE No Action
;

ALTER TABLE af.job_stat_factor ADD CONSTRAINT "FK_job_stat_factor_job"
	FOREIGN KEY (job_id) REFERENCES af.job (id) ON DELETE No Action ON UPDATE No Action
;

ALTER TABLE af.job_stat_factor ADD CONSTRAINT "FK_job_stat_factor_property"
	FOREIGN KEY (stat_factor) REFERENCES af.property (id) ON DELETE No Action ON UPDATE No Action
;

ALTER TABLE af.model_stat ADD CONSTRAINT "FK_model_stat_job"
	FOREIGN KEY (job_id) REFERENCES af.job (id) ON DELETE No Action ON UPDATE No Action
;

ALTER TABLE af.prediction ADD CONSTRAINT "FK_prediction_job_stat_factor"
	FOREIGN KEY (job_stat_factor_id) REFERENCES af.job_stat_factor (id) ON DELETE No Action ON UPDATE No Action
;

ALTER TABLE af.variance ADD CONSTRAINT "FK_variance_job"
	FOREIGN KEY (job_id) REFERENCES af.job (id) ON DELETE No Action ON UPDATE No Action
;

ALTER TABLE af.effect ADD CONSTRAINT "FK_effect_job_stat_factor"
	FOREIGN KEY (job_stat_factor_id) REFERENCES af.job_stat_factor (id) ON DELETE No Action ON UPDATE No Action
;

COMMENT ON COLUMN af.fitted_values.creation_timestamp
	IS 'Timestamp when the record was added to the table'
;

COMMENT ON COLUMN af.fitted_values.creator_id
	IS 'ID of the user who added the record to the table'
;

COMMENT ON COLUMN af.fitted_values.is_void
	IS 'Indicator whether the record is deleted (true) or not (false)'
;

COMMENT ON COLUMN af.fitted_values.modification_timestamp
	IS 'Timestamp when the record was last modified'
;

COMMENT ON COLUMN af.fitted_values.modifier_id
	IS 'ID of the user who last modified the record'
;

COMMENT ON COLUMN af.fitted_values.tenant_id
	IS 'Id of the selected Tenant'
;

COMMENT ON COLUMN af.job_data.creation_timestamp
	IS 'Timestamp when the record was added to the table'
;

COMMENT ON COLUMN af.job_data.creator_id
	IS 'ID of the user who added the record to the table'
;

COMMENT ON COLUMN af.job_data.is_void
	IS 'Indicator whether the record is deleted (true) or not (false)'
;

COMMENT ON COLUMN af.job_data.modification_timestamp
	IS 'Timestamp when the record was last modified'
;

COMMENT ON COLUMN af.job_data.modifier_id
	IS 'ID of the user who last modified the record'
;

COMMENT ON COLUMN af.job_data.tenant_id
	IS 'Id of the selected Tenant'
;

COMMENT ON COLUMN af.job_stat_factor.creation_timestamp
	IS 'Timestamp when the record was added to the table'
;

COMMENT ON COLUMN af.job_stat_factor.creator_id
	IS 'ID of the user who added the record to the table'
;

COMMENT ON COLUMN af.job_stat_factor.is_void
	IS 'Indicator whether the record is deleted (true) or not (false)'
;

COMMENT ON COLUMN af.job_stat_factor.modification_timestamp
	IS 'Timestamp when the record was last modified'
;

COMMENT ON COLUMN af.job_stat_factor.modifier_id
	IS 'ID of the user who last modified the record'
;

COMMENT ON COLUMN af.job_stat_factor.tenant_id
	IS 'Id of the selected Tenant'
;

COMMENT ON COLUMN af.model_stat.creation_timestamp
	IS 'Timestamp when the record was added to the table'
;

COMMENT ON COLUMN af.model_stat.creator_id
	IS 'ID of the user who added the record to the table'
;

COMMENT ON COLUMN af.model_stat.is_void
	IS 'Indicator whether the record is deleted (true) or not (false)'
;

COMMENT ON COLUMN af.model_stat.modification_timestamp
	IS 'Timestamp when the record was last modified'
;

COMMENT ON COLUMN af.model_stat.modifier_id
	IS 'ID of the user who last modified the record'
;

COMMENT ON COLUMN af.model_stat.tenant_id
	IS 'Id of the selected Tenant'
;

COMMENT ON COLUMN af.prediction.creation_timestamp
	IS 'Timestamp when the record was added to the table'
;

COMMENT ON COLUMN af.prediction.creator_id
	IS 'ID of the user who added the record to the table'
;

COMMENT ON COLUMN af.prediction.is_void
	IS 'Indicator whether the record is deleted (true) or not (false)'
;

COMMENT ON COLUMN af.prediction.modification_timestamp
	IS 'Timestamp when the record was last modified'
;

COMMENT ON COLUMN af.prediction.modifier_id
	IS 'ID of the user who last modified the record'
;

COMMENT ON COLUMN af.prediction.tenant_id
	IS 'Id of the selected Tenant'
;

COMMENT ON COLUMN af.variance.creation_timestamp
	IS 'Timestamp when the record was added to the table'
;

COMMENT ON COLUMN af.variance.creator_id
	IS 'ID of the user who added the record to the table'
;

COMMENT ON COLUMN af.variance.is_void
	IS 'Indicator whether the record is deleted (true) or not (false)'
;

COMMENT ON COLUMN af.variance.modification_timestamp
	IS 'Timestamp when the record was last modified'
;

COMMENT ON COLUMN af.variance.modifier_id
	IS 'ID of the user who last modified the record'
;

COMMENT ON COLUMN af.variance.tenant_id
	IS 'Id of the selected Tenant'
;

COMMENT ON COLUMN af.effect.creation_timestamp
	IS 'Timestamp when the record was added to the table'
;

COMMENT ON COLUMN af.effect.creator_id
	IS 'ID of the user who added the record to the table'
;

COMMENT ON COLUMN af.effect.is_void
	IS 'Indicator whether the record is deleted (true) or not (false)'
;

COMMENT ON COLUMN af.effect.modification_timestamp
	IS 'Timestamp when the record was last modified'
;

COMMENT ON COLUMN af.effect.modifier_id
	IS 'ID of the user who last modified the record'
;

COMMENT ON COLUMN af.effect.tenant_id
	IS 'Id of the selected Tenant'
;

--Revert Changes
--rollback DROP SEQUENCE af.fitted_values_id_seq;
--rollback DROP SEQUENCE af.job_data_id_seq;
--rollback DROP SEQUENCE af.job_stat_factor_id_seq;
--rollback DROP SEQUENCE af.model_stat_id_seq;
--rollback DROP SEQUENCE af.prediction_id_seq;
--rollback DROP SEQUENCE af.variance_id_seq;
--rollback DROP SEQUENCE af.effect_id_seq;

--rollback DROP TABLE af.effect;
--rollback DROP TABLE af.fitted_values;
--rollback DROP TABLE af.job_data;
--rollback DROP TABLE af.job_stat_factor CASCADE;
--rollback DROP TABLE af.model_stat;
--rollback DROP TABLE af.prediction;
--rollback DROP TABLE af.variance;


