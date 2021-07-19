--liquibase formatted sql

--changeset postgres:add_randprepirri_model context:template splitStatements:false rollbackSplitStatements:false
--comment: DB-244 Load Design data


/* new property randPREPirri*/
INSERT INTO af.property
(code, "name", "label", description, "type", data_type, creator_id, is_void, tenant_id, id, "statement")
VALUES('randPREPirri', 'randPREPirri', 'randPREPirri', NULL, 'catalog_item', 'integer', '1', false, 1, 168, NULL);

INSERT INTO af.property_config
(is_required, order_number, creation_timestamp, creator_id, is_void, tenant_id, id, property_id, config_property_id, property_ui_id, is_layout_variable)
VALUES(false, 8, now(), '1', false, 1, 274, 4, 168, NULL, false);

/*randPREPirri metadata*/
insert into af.property_meta(property_id,code,value,creation_timestamp,tenant_id) values
(168,'Rversion','4.0.3',now(),1),
(168,'date','23-Jan-2021',now(),1),
(168,'author','Alaine Gulles',now(),1),
(168,'email','a.gulles@irri.org',now(),1),
(168,'syntax','Rscript randPREPirri.R --entryList "PREP_SD_0001.lst" --nTrial 3 --genLayout F -o ''Output1'' -p ''D:/Results''" | "Rscript randPREPirri.R --entryList "PREP_SD_0001.lst" --nTrial 3 --genLayout T --nFieldRow 20 --serpentine ''CO'' -o ''Output2'' -p ''D:/Results''',now(),1),
(168,'engine','R 4.0.3',now(),1),
(168,'method','randPREPirri',now(),1),
(168,'design','PRep',now(),1),
(168,'modelVersion','1',now(),1),
(168,'organization_code','IRRI',now(),1),
(168,'note','Total number of plots per occurrence should not exceed 1,500.',now(),1);


/*randPREPirri new params*/
INSERT INTO af.property
(code, "name", "label", description, "type", data_type, creation_timestamp, modification_timestamp, creator_id, modifier_id, is_void, tenant_id, id, "statement")
VALUES
('checkList', 'checkList', 'Check Entry List', NULL, 'input', 'string', now(), NULL, '1', NULL, false, NULL, 169, NULL),
('testList', 'testList', 'Test Entry List', NULL, 'input', 'string', now(), NULL, '1', NULL, false, NULL, 170, NULL),
('serpentinePrep', 'serpentinePrep', 'Field Order', 'Plot arrangement', 'input', 'enumeration', now(), NULL, '1', NULL, false, NULL, 171, NULL),
('DesignArray', 'DesignArray', 'Randomization Fieldbook file', 'spreadsheet file showing the result of  the randomization (and layout, if generated)', 'output', 'csv', now(), NULL, '1', NULL, false, NULL, 172, NULL);


INSERT INTO af.property_ui
(id, is_visible, minimum, maximum, unit, "default", is_disabled, is_multiple, is_catalogue, creation_timestamp, modification_timestamp, creator_id, modifier_id, is_void, tenant_id)
VALUES
(78, false, null, null, null, null, true, false, false, now(), null, '1', null, false, 1),
(79, false, null, null, null, null, true, false, false, now(), null, '1', null, false, 1),
(80, false, null, null, null, null, true, false, false, now(), null, '1', null, false, 1),
(81, true, 1, null, null, '1', false, false, false, now(), null, '1', null, false, 1),
(82, true, null, null, null, 'F', false, false, false, now(), null, '1', null, false, 1),
(83, true, null, null, null, NULL, false, false, false, now(), null, '1', null, false, 1),
(84, true, null, null, null, NULL, false, false, false, now(), null, '1', null, false, 1),
(85, false, null, null, null, NULL, true, false, false, now(), null, '1', null, false, 1),
(86, false, null, null, null, NULL, true, false, false, now(), null, '1', null, false, 1)
;


INSERT INTO af.property_config
(is_required, order_number, creation_timestamp, modification_timestamp, creator_id, modifier_id, is_void, tenant_id, id, property_id, config_property_id, property_ui_id, is_layout_variable)
VALUES
(true, 1, now(), NULL, '1', NULL, false, 1, 275, 168, 66, 78, false),
(true, 2, now(), NULL, '1', NULL, false, 1, 276, 168, 169, 79, false),
(true, 3, now(), NULL, '1', NULL, false, 1, 277, 168, 170, 80, false),
(true, 4, now(), NULL, '1', NULL, false, 1, 278, 168, 65, 81, false),
(true, 5, now(), NULL, '1', NULL, false, 1, 279, 168, 68, 82, false),
(true, 6, now(), NULL, '1', NULL, false, 1, 280, 168, 69, 83, true),
(true, 7, now(), NULL, '1', NULL, false, 1, 281, 168, 171, 84, true),
(true, 8, now(), NULL, '1', NULL, false, 1, 282, 168, 72, 85, true),
(true, 9, now(), NULL, '1', NULL, false, 1, 283, 168, 73, 86, false),

(true, 1, now(), NULL, '1', NULL, false, 1, 284, 168, 172, null, false),
(true, 2, now(), NULL, '1', NULL, false, 1, 285, 168, 97, null, false)

;

INSERT INTO af.property_rule
("type", "expression", "group", creation_timestamp, modification_timestamp, creator_id, modifier_id, is_void, tenant_id, id, property_id, property_config_id, order_number, notification, "action")
VALUES
('validation-design', 'nCheck>1', null, now(), NULL, '1', NULL, false, 1, 79, NULL, 275, 1, 'Number of check entries should be greater than 1.', 'error'),
('validation-design', 'nTest>1', null, now(), NULL, '1', NULL, false, 1, 80, NULL, 275, 2, 'Number of test entries should be greater than 1.', 'error'),
('validation-design', 'nRep>1', null, now(), NULL, '1', NULL, false, 1, 81, NULL, 276, 1, 'Number of replicates for check entries should be at least 2.', 'error'),
('validation-design', 'nRep>1', null, now(), NULL, '1', NULL, false, 1, 82, NULL, 277, 1, 'Number of replicates for test entries should be at most 1.', 'error'),
('validation-design', '(nRep>=2)for(nTest*0.2)', null, now(), NULL, '1', NULL, false, 1, 83, NULL, 277, 2, 'At least 20% of the test entries shoulde have at most 2 number of replicates.', 'error')
;

select setval('af.property_rule_id_seq',max(id)) from af.property_rule;
select setval('af.property_config_id_seq',max(id)) from af.property_config;
select setval('af.property_ui_id_seq',max(id)) from af.property_ui;
select setval('af.property_id_seq',max(id)) from af.property;
select setval('af.property_meta_id_seq',max(id)) from af.property_meta;


--Revert Changes
--rollback DELETE FROM af.property_rule WHERE id IN(79,80,81,82,83);
--rollback DELETE FROM af.property_config WHERE id IN(275,276,277,278,279,280,281,282,283,284,285);
--ROLLBACK DELETE FROM af.property_ui WHERE id IN(78,79,80,81,82,83,84,85,86);
--rollback DELETE FROM af.property WHERE id IN (169,170,171,172);
--rollback DELETE FROM af.property_meta WHERE property_id = 168;
--rollback DELETE FROM af.property_config WHERE id =274;
--rollback DELETE FROM af.property WHERE id = 168;

