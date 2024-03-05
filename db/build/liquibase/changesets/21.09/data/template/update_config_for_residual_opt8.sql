--liquibase formatted sql

--changeset postgres:update_config_for_residual_opt8 context:template splitStatements:false rollbackSplitStatements:false
--comment: DB-697 Update property_config of property residual_opt8


UPDATE af.property_config
SET config_property_id=192
WHERE id=254;

UPDATE af.property_config
SET config_property_id=192
WHERE id=271;


--Revert Changes
--rollback UPDATE af.property_config SET config_property_id=155 WHERE id=254;
--rollback UPDATE af.property_config SET config_property_id=155 WHERE id=271;
