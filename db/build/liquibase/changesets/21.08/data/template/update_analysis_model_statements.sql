--liquibase formatted sql

--changeset postgres:update_analysis_model_statements context:template splitStatements:false rollbackSplitStatements:false
--comment: BA-602 Update analysis model statements/data type



UPDATE af.property
SET  "statement" = 'units'
WHERE id=155;

UPDATE af.property
SET data_type='*' 
WHERE id=164;

--Revert Changes
--rollback UPDATE af.property SET  "statement" = NULL WHERE id=155;
--rollback UPDATE af.property SET data_type='!I' WHERE id=164;