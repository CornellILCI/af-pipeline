--liquibase formatted sql

--changeset postgres:change_varchar_columns_to_text_columns context:schema splitStatements:false rollbackSplitStatements:false
--comment: BA-578 Chnage columns of type VARCHAR to columns of type TEXT


ALTER TABLE af.analysis
    ALTER COLUMN name TYPE text,
    ALTER COLUMN description TYPE text,
    ALTER COLUMN status TYPE text,
    ALTER COLUMN creator_id TYPE text,
    ALTER COLUMN modifier_id TYPE text;
