--liquibase formatted sql

--changeset postgres:change_varchar_columns_to_text_columns context:schema splitStatements:false rollbackSplitStatements:false
--comment: BA-578 Chnage columns of type VARCHAR to columns of type TEXT


ALTER TABLE af.analysis
    ALTER COLUMN name TYPE text,
    ALTER COLUMN description TYPE text,
    ALTER COLUMN status TYPE text,
    ALTER COLUMN creator_id TYPE text,
    ALTER COLUMN modifier_id TYPE text;


ALTER TABLE af.effect
    ALTER COLUMN type TYPE text,
    ALTER COLUMN creator_id TYPE text,
    ALTER COLUMN modifier_id TYPE text;


ALTER TABLE af.job
    ALTER COLUMN name TYPE text,
    ALTER COLUMN time_start TYPE text,
    ALTER COLUMN time_end TYPE text,
    ALTER COLUMN output_path TYPE text,
    ALTER COLUMN status TYPE text,
    ALTER COLUMN status_message TYPE text,
    ALTER COLUMN size TYPE text,
    ALTER COLUMN creator_id TYPE text,
    ALTER COLUMN modifier_id TYPE text;


ALTER TABLE af.job_data
    ALTER COLUMN data TYPE text,
    ALTER COLUMN creator_id TYPE text,
    ALTER COLUMN modifier_id TYPE text;


ALTER TABLE af.job_stat_factor
    ALTER COLUMN creator_id TYPE text,
    ALTER COLUMN modifier_id TYPE text;


