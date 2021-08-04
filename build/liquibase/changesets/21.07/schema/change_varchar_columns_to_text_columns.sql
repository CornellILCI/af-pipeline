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


ALTER TABLE af.model_stat
    ALTER COLUMN log_lik TYPE text,
    ALTER COLUMN aic TYPE text,
    ALTER COLUMN bic TYPE text,
    ALTER COLUMN creator_id TYPE text,
    ALTER COLUMN modifier_id TYPE text;


ALTER TABLE af.prediction
    ALTER COLUMN value TYPE text,
    ALTER COLUMN std_error TYPE text,
    ALTER COLUMN e_code TYPE text,
    ALTER COLUMN ci95_upper TYPE text,
    ALTER COLUMN ci95_lower TYPE text,
    ALTER COLUMN creator_id TYPE text,
    ALTER COLUMN modifier_id TYPE text;


ALTER TABLE af.property
    ALTER COLUMN code TYPE text,
    ALTER COLUMN name TYPE text,
    ALTER COLUMN label TYPE text,
    ALTER COLUMN description TYPE text,
    ALTER COLUMN type TYPE text,
    ALTER COLUMN data_type TYPE text,
    ALTER COLUMN creator_id TYPE text,
    ALTER COLUMN modifier_id TYPE text;


ALTER TABLE af.property_acl
    ALTER COLUMN creator_id TYPE text,
    ALTER COLUMN modifier_id TYPE text;


ALTER TABLE af.property_config
    ALTER COLUMN creator_id TYPE text,
    ALTER COLUMN modifier_id TYPE text;


ALTER TABLE af.property_meta
    ALTER COLUMN code TYPE text,
    ALTER COLUMN value TYPE text,
    ALTER COLUMN creator_id TYPE text,
    ALTER COLUMN modifier_id TYPE text;


ALTER TABLE af.property_rule
    ALTER COLUMN type TYPE text,
    ALTER COLUMN expression TYPE text,
    ALTER COLUMN notification TYPE text,
    ALTER COLUMN action TYPE text,
    ALTER COLUMN creator_id TYPE text,
    ALTER COLUMN modifier_id TYPE text;


ALTER TABLE af.property_ui
    ALTER COLUMN unit TYPE text,
    ALTER COLUMN default TYPE text,
    ALTER COLUMN creator_id TYPE text,
    ALTER COLUMN modifier_id TYPE text;


ALTER TABLE af.request
    ALTER COLUMN uuid TYPE text,
    ALTER COLUMN category TYPE text,
    ALTER COLUMN type TYPE text,
    ALTER COLUMN design TYPE text,
    ALTER COLUMN requestor_id TYPE text,
    ALTER COLUMN institute TYPE text,
    ALTER COLUMN requestor_id TYPE text,
    ALTER COLUMN institute TYPE text,
    ALTER COLUMN crop TYPE text,
    ALTER COLUMN program TYPE text,
    ALTER COLUMN status TYPE text,
    ALTER COLUMN engine TYPE text,
    ALTER COLUMN msg TYPE text,
    ALTER COLUMN creator_id TYPE text,
    ALTER COLUMN modifier_id TYPE text;


ALTER TABLE af.request_entry
    ALTER COLUMN creator_id TYPE text,
    ALTER COLUMN modifier_id TYPE text;


ALTER TABLE af.request_parameter
    ALTER COLUMN value TYPE text,
    ALTER COLUMN creator_id TYPE text,
    ALTER COLUMN modifier_id TYPE text;


ALTER TABLE af.task
    ALTER COLUMN name TYPE text,
    ALTER COLUMN status TYPE text,
    ALTER COLUMN err_msg TYPE text,
    ALTER COLUMN processor TYPE text,
    ALTER COLUMN creator_id TYPE text,
    ALTER COLUMN modifier_id TYPE text;


ALTER TABLE af.variance
    ALTER COLUMN source TYPE text,
    ALTER COLUMN model TYPE text,
    ALTER COLUMN gamma TYPE text,
    ALTER COLUMN component TYPE text,
    ALTER COLUMN component_ratio TYPE text,
    ALTER COLUMN last_change_percentage TYPE text,
    ALTER COLUMN code TYPE text,
    ALTER COLUMN creator_id TYPE text,
    ALTER COLUMN modifier_id TYPE text;
