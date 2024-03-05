--liquibase formatted sql

--changeset postgres:set_is_void_false_property_ui_and_meta context:template splitStatements:false rollbackSplitStatements:false
--comment: BA-461 Set is_void=false in badb tables


UPDATE af.property_meta
SET is_void = false;

UPDATE af.property_ui
SET is_void = false;


--Revert Changes
--rollback UPDATE af.property_meta SET is_void = NULL WHERE id <= 66;
--rollback UPDATE af.property_ui SET is_void = NULL WHERE id <= 76;