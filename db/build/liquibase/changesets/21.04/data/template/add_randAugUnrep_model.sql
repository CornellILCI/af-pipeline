--liquibase formatted sql

--changeset postgres:add_randAugUnrep_model context:template splitStatements:false rollbackSplitStatements:false
--comment: DB-244 Load Design data


/* new property randPREPirri*/
INSERT INTO af.property
(code, "name", "label", description, "type", data_type, creator_id, is_void, tenant_id, id, "statement")
VALUES('randAugUnrep', 'randAugUnrep', 'randPREPirri', NULL, 'catalog_item', 'integer', '1', false, 1, 173, NULL);

INSERT INTO af.property_config
(is_required, order_number, creation_timestamp, creator_id, is_void, tenant_id, id, property_id, config_property_id, property_ui_id, is_layout_variable)
VALUES(false, 9, now(), '1', false, 1, 286, 4, 173, NULL, false);

/*randPREPirri metadata*/
insert into af.property_meta(property_id,code,value,creation_timestamp,tenant_id) values
(173,'Rversion','4.0.2',now(),1),
(173,'date','07-Mar-2021',now(),1),
(173,'author','Pedro Augusto Medeiros Barbosa',now(),1),
(173,'email','p.medeiros@cgiar.org',now(),1),
(173,'syntax','Rscript randAugUnrep.R --entryList ''AugUnrep_SD_0001.lst'' --nTrial 3 --pCheck 10 --nFieldCol 20',now(),1),
(173,'engine','R 4.0.2',now(),1),
(173,'method','randAugUnrep',now(),1),
(173,'design','Augmented Design diagonal chekcs',now(),1),
(173,'modelVersion','1',now(),1),
(173,'organization_code','CIMMYT',now(),1),
(173,'note',' ',now(),1);


/*randPREPirri new params*/
INSERT INTO af.property
(code, "name", "label", description, "type", data_type, creation_timestamp, modification_timestamp, creator_id, modifier_id, is_void, tenant_id, id, "statement")
VALUES
('nFieldCol', 'nFieldCol', 'Columns', 'Total number of columns', 'input', 'integer', now(), NULL, '1', NULL, false, 1, 174, NULL),
('pCheck', 'pCheck', 'Percentage of check plots', 'Percentage of the total plots that spatial check entries will be assigned to (diagonal)', 'input', 'enumeration', now(), NULL, '1', NULL, false, NULL, 175, NULL)
;


INSERT INTO af.property_ui
(id, is_visible, minimum, maximum, unit, "default", is_disabled, is_multiple, is_catalogue, creation_timestamp, modification_timestamp, creator_id, modifier_id, is_void, tenant_id)
VALUES
(87, true, 1, null, null, '1', false, false, false, now(), null, '1', null, false, 1),
(88, false, null, null, null, null, true, false, false, now(), null, '1', null, false, 1),
(89, false, null, null, null, null, true, false, false, now(), null, '1', null, false, 1),
(90, true, 10, null, null, '20', false, false, false, now(), null, '1', null, false, 1),
(91, true, 5, 20, null, '10', false, false, false, now(), null, '1', null, false, 1),
(92, false, null, null, null, NULL, true, false, false, now(), null, '1', null, false, 1),
(93, false, null, null, null, NULL, true, false, false, now(), null, '1', null, false, 1)
;


INSERT INTO af.property_config
(is_required, order_number, creation_timestamp, modification_timestamp, creator_id, modifier_id, is_void, tenant_id, id, property_id, config_property_id, property_ui_id, is_layout_variable)
VALUES
(true, 1, now(), NULL, '1', NULL, false, 1, 287, 173, 65, 87, false),
(true, 2, now(), NULL, '1', NULL, false, 1, 288, 173, 66, 88, false),
(true, 3, now(), NULL, '1', NULL, false, 1, 289, 173, 169, 89, false),
(true, 4, now(), NULL, '1', NULL, false, 1, 290, 173, 174, 90, true),
(true, 5, now(), NULL, '1', NULL, false, 1, 291, 173, 175, 91, true),
(true, 6, now(), NULL, '1', NULL, false, 1, 292, 173, 72, 92, false),
(true, 7, now(), NULL, '1', NULL, false, 1, 293, 173, 73, 93, false),

(true, 1, now(), NULL, '1', NULL, false, 1, 294, 173, 172, null, false),
(true, 2, now(), NULL, '1', NULL, false, 1, 295, 173, 97, null, false)
;

INSERT INTO af.property_rule
("type", "expression", "group", creation_timestamp, modification_timestamp, creator_id, modifier_id, is_void, tenant_id, id, property_id, property_config_id, order_number, notification, "action")
VALUES
('validation-design', 'nCheck>1', null, now(), NULL, '1', NULL, false, 1, 84, NULL, 288, 1, 'Number of check entries should be greater than 1.', 'error'),
('validation-design', 'nEntries>50', null, now(), NULL, '1', NULL, false, 1, 85, NULL, 288, 2, 'Number of test entries should be greater than 50.', 'error'),
('validation-design', 'nSpatialCheck>2', null, now(), NULL, '1', NULL, false, 1, 86, NULL, 289, 1, 'Number of entries used as spatial checks must be at least 2.', 'error')
;


select setval('af.property_rule_id_seq',max(id)) from af.property_rule;
select setval('af.property_config_id_seq',max(id)) from af.property_config;
select setval('af.property_ui_id_seq',max(id)) from af.property_ui;
select setval('af.property_id_seq',max(id)) from af.property;
select setval('af.property_meta_id_seq',max(id)) from af.property_meta;


--Revert Changes
--rollback DELETE FROM af.property_rule WHERE id IN(84,85,86);
--rollback DELETE FROM af.property_config WHERE id IN(287,288,289,290,291,292,293,294,295);
--ROLLBACK DELETE FROM af.property_ui WHERE id IN(87,88,89,90,91,92,93);
--rollback DELETE FROM af.property WHERE id IN (174,175);
--rollback DELETE FROM af.property_meta WHERE property_id = 173;
--rollback DELETE FROM af.property_config WHERE id =286;
--rollback DELETE FROM af.property WHERE id = 173;


