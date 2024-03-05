--liquibase formatted sql

--changeset postgres:add_values_in_serpentine_and_pcheck context:template splitStatements:false rollbackSplitStatements:false
--comment: DB-244 Load Design data



/*serpentinePrep values*/
INSERT INTO af.property
(code, "name", "label", description, "type", data_type, creation_timestamp, modification_timestamp, creator_id, modifier_id, is_void, tenant_id, id, "statement")
VALUES
('CS', 'Column Serpentine', 'Column Serpentine', 'value', 'input', 'character', now(), NULL, '1', NULL, false, 1, 176, NULL),
('CO', 'Column Order', 'Column Order', 'value', 'input', 'character', now(), NULL, '1', NULL, false, 1, 177, NULL),
('RS', 'Row Serpentine', 'Row Serpentine', 'value', 'input', 'character', now(), NULL, '1', NULL, false, 1, 178, NULL),
('RO', 'Row Order', 'Row Order', 'value', 'input', 'character', now(), NULL, '1', NULL, false, 1, 179, NULL);

INSERT INTO af.property_config
(is_required, order_number, creation_timestamp, modification_timestamp, creator_id, modifier_id, is_void, tenant_id, id, property_id, config_property_id, property_ui_id, is_layout_variable)
VALUES
(true, 1, now(), NULL, '1', NULL, false, 1, 296, 171, 176, NULL, false),
(true, 2, now(), NULL, '1', NULL, false, 1, 297, 171, 177, NULL, false),
(true, 3, now(), NULL, '1', NULL, false, 1, 298, 171, 178, NULL, false),
(true, 4, now(), NULL, '1', NULL, false, 1, 299, 171, 179, NULL, false);


/*pCheck values*/
INSERT INTO af.property
(code, "name", "label", description, "type", data_type, creation_timestamp, modification_timestamp, creator_id, modifier_id, is_void, tenant_id, id, "statement")
VALUES
('5%', '5', '5', 'value', 'input', 'integer', now(), NULL, '1', NULL, false, 1, 180, NULL),
('6%', '6', '6', 'value', 'input', 'integer', now(), NULL, '1', NULL, false, 1, 181, NULL),
('7%', '7', '7', 'value', 'input', 'integer', now(), NULL, '1', NULL, false, 1, 182, NULL),
('8%', '8', '8', 'value', 'input', 'integer', now(), NULL, '1', NULL, false, 1, 183, NULL),
('9%', '9', '9', 'value', 'input', 'integer', now(), NULL, '1', NULL, false, 1, 184, NULL),
('10%', '10', '10', 'value', 'input', 'integer', now(), NULL, '1', NULL, false, 1, 185, NULL),
('11%', '11', '11', 'value', 'input', 'integer', now(), NULL, '1', NULL, false, 1, 186, NULL),
('12%', '12', '12', 'value', 'input', 'integer', now(), NULL, '1', NULL, false, 1, 187, NULL),
('13%', '13', '13', 'value', 'input', 'integer', now(), NULL, '1', NULL, false, 1, 188, NULL),
('14%', '14', '14', 'value', 'input', 'integer', now(), NULL, '1', NULL, false, 1, 189, NULL),
('15%', '15', '15', 'value', 'input', 'integer', now(), NULL, '1', NULL, false, 1, 190, NULL),
('20%', '20', '20', 'value', 'input', 'integer', now(), NULL, '1', NULL, false, 1, 191, NULL);


INSERT INTO af.property_config
(is_required, order_number, creation_timestamp, modification_timestamp, creator_id, modifier_id, is_void, tenant_id, id, property_id, config_property_id, property_ui_id, is_layout_variable)
VALUES
(true, 1, now(), NULL, '1', NULL, false, 1, 300, 175, 180, NULL, false),
(true, 2, now(), NULL, '1', NULL, false, 1, 301, 175, 181, NULL, false),
(true, 3, now(), NULL, '1', NULL, false, 1, 302, 175, 182, NULL, false),
(true, 4, now(), NULL, '1', NULL, false, 1, 303, 175, 183, NULL, false),
(true, 5, now(), NULL, '1', NULL, false, 1, 304, 175, 184, NULL, false),
(true, 6, now(), NULL, '1', NULL, false, 1, 305, 175, 185, NULL, false),
(true, 7, now(), NULL, '1', NULL, false, 1, 306, 175, 186, NULL, false),
(true, 8, now(), NULL, '1', NULL, false, 1, 307, 175, 187, NULL, false),
(true, 9, now(), NULL, '1', NULL, false, 1, 308, 175, 188, NULL, false),
(true, 10, now(), NULL, '1', NULL, false, 1, 309, 175, 189, NULL, false),
(true, 11, now(), NULL, '1', NULL, false, 1, 310, 175, 190, NULL, false),
(true, 12, now(), NULL, '1', NULL, false, 1, 311, 175, 191, NULL, false)
;


select setval('af.property_config_id_seq',max(id)) from af.property_config;
select setval('af.property_id_seq',max(id)) from af.property;


--Revert Changes
--rollback DELETE FROM af.property_config WHERE id >=300;
--rollback DELETE FROM af.property WHERE id>=180;
--rollback DELETE FROM af.property_config WHERE id >=296;
--rollback DELETE FROM af.property WHERE id >= 176;
