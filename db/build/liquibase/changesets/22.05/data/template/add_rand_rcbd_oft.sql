--liquibase formatted sql

--changeset postgres:add_rand_rcbd_oft context:template splitStatements:false rollbackSplitStatements:false
--comment: BA2-89 SDM: Add the On-Farm trial to the DB



/* new property randRCBDirri_OFT */
WITH design AS (
    INSERT INTO af.property
        (code, "name", "label", description, "type", data_type, creator_id, is_void, tenant_id
    )VALUES
        ('randRCBDirri_OFT', 'randRCBDirri_OFT', 'Entry List', 'CSV file with the entries information', 'catalog_item', 'integer', '1', false, 1)
	RETURNING id
)

INSERT INTO af.property_config
    (is_required, order_number, creator_id, is_void, tenant_id, property_id, config_property_id, is_layout_variable)
VALUES
    (false, 11, '1', false, 1, 4, (select id from design), false)
;


/*randRCBDirri_OFT metadata*/
WITH model_design AS (
	SELECT id FROM af.property WHERE code = 'randRCBDirri_OFT'
)
INSERT INTO af.property_meta(code,value,property_id) VALUES
	('Rversion', '4.1.1', (SELECT id FROM model_design)),
	('date', '26-Apr-2022', (SELECT id FROM model_design)),
	('author', 'Alaine Gulles', (SELECT id FROM model_design)),
	('email', 'a.gulles@irri.org', (SELECT id FROM model_design)),
	('syntax', 'Rscript randRCBD_OFT.R --entryList "RCBD_OFT_SD_0001.lst" --nTrial 3 -o "Output1" -p "D:/Results"', (SELECT id FROM model_design)),
    ('engine',  'R 4.1.1', (SELECT id FROM model_design)),
	('method', 'randRCBD_OFT', (SELECT id FROM model_design)),
    ('stage', 'OFT', (SELECT id FROM model_design)),
    ('design', 'Randomized Complete Block', (SELECT id FROM model_design)),
    ('modelVersion', '1', (SELECT id FROM model_design)),
    ('organization_code', 'IRRI', (SELECT id FROM model_design)),
    ('note', '', (SELECT id FROM model_design));



--Entry list--
WITH property_ui AS (
    INSERT INTO af.property_ui
        (is_visible, minimum, maximum, unit, "default", is_disabled, is_multiple, is_catalogue, creator_id, is_void, tenant_id)
    VALUES
        (false, null, null, null, null, true, false, false, '1', false, 1)
	RETURNING id
), property_conf AS (
    INSERT INTO af.property_config
        (is_required, order_number, creator_id, is_void, tenant_id, property_id, config_property_id, property_ui_id, is_layout_variable)
    VALUES
        (true, 1, '1', false, 1, (SELECT id FROM af.property WHERE code = 'randRCBDirri_OFT'), 66, (select id from property_ui), false)
    RETURNING id
)

INSERT INTO af.property_rule
("type", "expression", "group", creator_id, is_void, tenant_id, property_id, property_config_id, order_number, notification, "action")
VALUES
('validation-design', 'nCheck>1', null, '1', false, 1, NULL, (select id from property_conf), 1, 'Total number of check entries should be greated than 1.', 'error'),
('validation-design', 'nEntries>3', null, '1', false, 1, NULL, (select id from property_conf), 2, 'Total number of test entries should be at least 3.', 'error'),
('validation-design', 'totalEntries>=5', null, '1', false, 1, NULL, (select id from property_conf), 3, 'Minimum number of entries should be 5.', 'warning'),
('validation-design', 'totalEntries<=15', null, '1', false, 1, NULL, (select id from property_conf), 4, 'Total number of entries is too large for OFT. Usually OFT evaluates at most 15 entries.', 'warning')
;


--nFarm--
WITH property_ui AS (
    INSERT INTO af.property_ui
        (is_visible, minimum, maximum, unit, "default", is_disabled, is_multiple, is_catalogue, creator_id, is_void, tenant_id)
    VALUES
        (true, 10, null, null, '10', false, false, false, '1', false, 1)
	RETURNING id
)

INSERT INTO af.property_config
    (is_required, order_number, creator_id, is_void, tenant_id, property_id, config_property_id, property_ui_id, is_layout_variable)
VALUES
    (true, 2, '1', false, 1, (SELECT id FROM af.property WHERE code = 'randRCBDirri_OFT'), (select id from af.property where code = 'nFarm'), (select id from property_ui), false)
;



--output file--
WITH property_ui AS (
    INSERT INTO af.property_ui
        (is_visible, minimum, maximum, unit, "default", is_disabled, is_multiple, is_catalogue, creator_id, is_void, tenant_id)
    VALUES
        (false, null, null, null, null, true, false, false, '1', false, 1)
	RETURNING id
)

INSERT INTO af.property_config
    (is_required, order_number, creator_id, is_void, tenant_id, property_id, config_property_id, property_ui_id, is_layout_variable)
VALUES
    (true, 3, '2', false, 1, (SELECT id FROM af.property WHERE code = 'randRCBDirri_OFT'), 72, (select id from property_ui), false)
;



--output path--
WITH property_ui AS (
    INSERT INTO af.property_ui
        (is_visible, minimum, maximum, unit, "default", is_disabled, is_multiple, is_catalogue, creator_id, is_void, tenant_id)
    VALUES
        (false, null, null, null, null, true, false, false, '1', false, 1)
	RETURNING id
)

INSERT INTO af.property_config
    (is_required, order_number, creator_id, is_void, tenant_id, property_id, config_property_id, property_ui_id, is_layout_variable)
VALUES
    (true, 4, '1', false, 1, (SELECT id FROM af.property WHERE code = 'randRCBDirri_OFT'), 73, (select id from property_ui), false)
;



--DesignArray--
INSERT INTO af.property_config
    (is_required, order_number, creator_id, is_void, tenant_id, property_id, config_property_id, property_ui_id, is_layout_variable)
VALUES
    (true, 5, '1', false, 1, (SELECT id FROM af.property WHERE code = 'randRCBDirri_OFT'), 172, null, false)
;



--DesigInfo--
INSERT INTO af.property_config
    (is_required, order_number, creator_id, is_void, tenant_id, property_id, config_property_id, property_ui_id, is_layout_variable)
VALUES
    (true, 6, '1', false, 1, (SELECT id FROM af.property WHERE code = 'randRCBDirri_OFT'), 97, null, false)
;