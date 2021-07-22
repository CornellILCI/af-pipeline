--liquibase formatted sql

--changeset postgres:add_additional_info_to_fitted_values context:schema splitStatements:false rollbackSplitStatements:false
--comment: BA-496 add additional_info to fitted_values table

ALTER TABLE af.fitted_values
    ADD COLUMN additional_info jsonb;