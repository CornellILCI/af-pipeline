--liquibase formatted sql

--changeset postgres:update_ntrial_nrep_default_value_randrcbdirri context:template splitStatements:false rollbackSplitStatements:false
--comment: DB-539 Update default values for 2 fields in randRCBDirri


UPDATE af.property_ui
SET "default" = 1
WHERE id=7;

UPDATE af.property_ui
SET "default"= 2
WHERE id=9;



--Revert Changes
--rollback UPDATE af.property_ui SET "default" = NULL WHERE id=7;
--rollback UPDATE af.property_ui SET "default"= NULL WHERE id=9;