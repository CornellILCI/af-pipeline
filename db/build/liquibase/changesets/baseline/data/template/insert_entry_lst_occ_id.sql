--liquibase formatted sql

--changeset postgres:insert_entry_lst_occ_id context:template splitStatements:false rollbackSplitStatements:false
--comment: insert_entry_lst_occ_id



INSERT INTO af.property
(id, code, "name", "label", description, "type", data_type, creation_timestamp, modification_timestamp, creator_id, modifier_id, is_void, tenant_id)
VALUES(131, 'occurrenceId', 'OCC_ID', 'Occurrence Id', NULL, 'request_meta', 'integer', NULL, NULL, NULL, NULL, false, NULL);
INSERT INTO af.property
(id, code, "name", "label", description, "type", data_type, creation_timestamp, modification_timestamp, creator_id, modifier_id, is_void, tenant_id)
VALUES(132, 'entryListName', 'ENT_LST_NAME', 'Entry List Name', NULL, 'request_meta', 'character varying', NULL, NULL, NULL, NULL, false, NULL);

select setval('af.property_id_seq',max(id)) from af.property;