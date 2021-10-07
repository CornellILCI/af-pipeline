--liquibase formatted sql

--changeset postgres:assign_property_residual_and_asrmel context:template splitStatements:false rollbackSplitStatements:false
--comment: DB-696 Add property for residual and asreml option



INSERT INTO af.property_config
(is_required, order_number, creator_id, is_void, tenant_id, property_id, config_property_id, property_ui_id, is_layout_variable)
VALUES
(false, 1, '1', false, 1, 140, 192, NULL, false),
(false, 11, '1', false, 1, 137, 193, NULL, false);

select setval('af.property_config_id_seq',max(id)) from af.property_config;


--Revert Changes
--rollback DELETE FROM af.property_config WHERE property_id = 140 and config_property_id =192;
--rollback DELETE FROM af.property_config WHERE property_id = 137 and config_property_id =193;
--rollback select setval('af.property_config_id_seq',max(id)) from af.property_config;