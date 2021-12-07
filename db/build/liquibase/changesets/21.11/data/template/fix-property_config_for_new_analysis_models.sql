--liquibase formatted sql

--changeset postgres:fix-property_config_for_new_analysis_models context:template splitStatements:false rollbackSplitStatements:false
--comment: BA-795 Fix property_config for the new analysis models



UPDATE af.property_config SET property_id=134 WHERE id=312;

UPDATE af.property_config SET property_id=134 WHERE id=313;

UPDATE af.property_config SET property_id=134 WHERE id=352;

UPDATE af.property_config SET property_id=134 WHERE id=353;


--Revert Changes
--rollback UPDATE af.property_config SET property_id=4 WHERE id=312;
--rollback UPDATE af.property_config SET property_id=4 WHERE id=313;
--rollback UPDATE af.property_config SET property_id=4 WHERE id=352;
--rollback UPDATE af.property_config SET property_id=4 WHERE id=353;