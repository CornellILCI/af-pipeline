--liquibase formatted sql

--changeset postgres:add_additional_info_column_to_model_stat_table context:schema splitStatements:false rollbackSplitStatements:false
--comment: BA-576 add additional_info column to model_stat table

ALTER TABLE af.model_stat 
 ADD COLUMN aditional_info jsonb NULL;

COMMENT ON COLUMN af.model_stat.aditional_info IS 'Additional information';

--Revert CHnages
--rollback ALTER TABLE af.model_stat DROP COLUMN aditional_info;
