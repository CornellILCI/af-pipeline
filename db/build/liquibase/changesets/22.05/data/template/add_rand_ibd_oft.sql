--liquibase formatted sql

--changeset postgres:add_rand_ibd_oft context:template splitStatements:false rollbackSplitStatements:false
--comment: BA2-89 SDM: Add the On-Farm trial to the DB



/* new property randIBD_OFT */
WITH design AS (
    INSERT INTO af.property
        (code, "name", "label", description, "type", data_type, creator_id, is_void, tenant_id
    )VALUES
        ('randIBD_OFT', 'randIBD_OFT', 'No. farms', 'Number of participant farms.', 'catalog_item', 'integer', '1', false, 1)
	RETURNING id
)

INSERT INTO af.property_config
    (is_required, order_number, creator_id, is_void, tenant_id, property_id, config_property_id, is_layout_variable)
VALUES
    (false, 10, '1', false, 1, 4, (select id from design), false)
;


/*randIBD_OFT meta data*/
WITH model_design AS (
	SELECT id FROM af.property WHERE code = 'randIBD_OFT'
)
INSERT INTO af.property_meta(code,value,property_id) VALUES
	('Rversion', '4.1.3', (SELECT id FROM model_design)),
	('date', '22-Apr-2022', (SELECT id FROM model_design)),
	('author', 'Pedro Barbosa', (SELECT id FROM model_design)),
	('email', 'p.medeiros@cgiar.org', (SELECT id FROM model_design)),
	('syntax', 'Rscript randIBD_OFT.R -e randIBD_OFT_SD_0001.lst --sBlk 3 --nTrial 100', (SELECT id FROM model_design)),
    ('engine',  'R 4.1.3', (SELECT id FROM model_design)),
	('method', 'randIBD_OFT', (SELECT id FROM model_design)),
    ('stage', 'OFT', (SELECT id FROM model_design)),
    ('design', 'Incomplete Block', (SELECT id FROM model_design)),
    ('modelVersion', '1', (SELECT id FROM model_design)),
    ('organization_code', 'CIMMYT', (SELECT id FROM model_design)),
    ('note', '', (SELECT id FROM model_design));



--nFarm--
WITH property_ui AS (
    INSERT INTO af.property_ui
        (is_visible, minimum, maximum, unit, "default", is_disabled, is_multiple, is_catalogue, creator_id, is_void, tenant_id)
    VALUES
        (true, 60, null, null, '100', false, false, false, '1', false, 1)
	RETURNING id
), nfarm AS (
    INSERT INTO af.property
        (code, "name", "label", description, "type", data_type, creator_id, is_void, tenant_id)
    VALUES 
        ('nFarm', 'OCCURRENCES', 'No. of farms', 'Number of farms.', 'input', 'integer', '1', false, 1)
    RETURNING id
)
INSERT INTO af.property_config
    (is_required, order_number, creator_id, is_void, tenant_id, property_id, config_property_id, property_ui_id, is_layout_variable)
VALUES
    (true, 1, '1', false, 1, (SELECT id FROM af.property WHERE code = 'randIBD_OFT'), (select id from nfarm), (select id from property_ui), false)
;


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
        (true, 2, '1', false, 1, (SELECT id FROM af.property WHERE code = 'randIBD_OFT'), 66, (select id from property_ui), false)
    RETURNING id
)

INSERT INTO af.property_rule
("type", "expression", "group", creator_id, is_void, tenant_id, property_id, property_config_id, order_number, notification, "action")
VALUES
('validation-design', 'nCheck>2', null, '1', false, 1, NULL, (select id from property_conf), 1, 'Number of check entries should be greater than 2.', 'error'),
('validation-design', 'nEntries>2', null, '1', false, 1, NULL, (select id from property_conf), 2, 'Number of test entries should be greater than 2.', 'error'),
('validation-design', 'totalEntries>15', null, '1', false, 1, NULL, (select id from property_conf), 3, 'Total number of entries is too large. Usually OFT evaluates less than 15 genotypes', 'warning')
;


--plotFarm--
WITH property_ui AS (
    INSERT INTO af.property_ui
        (is_visible, minimum, maximum, unit, "default", is_disabled, is_multiple, is_catalogue, creator_id, is_void, tenant_id)
    VALUES
        (true, 3, null, null, null, false, false, false, '1', false, 1)
	RETURNING id
), plotfarm AS (
    INSERT INTO af.property
        (code, "name", "label", description, "type", data_type, creator_id, is_void, tenant_id)
    VALUES
        ('plotFarm', 'BLOCK_SIZE', 'No. of plots per farm', 'It is the number of plots per block in the Incomplete Block Design. In the case of OFT this is the number os genotypes evaluated in each farm', 'input', 'integer', '1', false, 1)
    RETURNING id
),property_conf AS (
    INSERT INTO af.property_config
        (is_required, order_number, creator_id, is_void, tenant_id, property_id, config_property_id, property_ui_id, is_layout_variable)
    VALUES
        (true, 3, '1', false, 1, (SELECT id FROM af.property WHERE code = 'randIBD_OFT'), (select id from plotfarm), (select id from property_ui), false)
    RETURNING id
)

INSERT INTO af.property_rule
("type", "expression", "group", creator_id, is_void, tenant_id, property_id, property_config_id, order_number, notification, "action")
VALUES
('allowed-value', 'value>2', null, '1', false, 1, NULL, (select id from property_conf), 1, null, null),
('allowed-value', 'value<(totalEntries)', null, '1', false, 1, NULL, (select id from property_conf), 2, null, null),
('allowed-value', 'value<nTest', null, '1', false, 1, NULL, (select id from property_conf), 3, null, null),
('allowed-value', 'value<nCheck', null, '1', false, 1, NULL, (select id from property_conf), 4, null, null)
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
    (true, 4, '1', false, 1, (SELECT id FROM af.property WHERE code = 'randIBD_OFT'), 72, (select id from property_ui), false)
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
    (true, 5, '1', false, 1, (SELECT id FROM af.property WHERE code = 'randIBD_OFT'), 73, (select id from property_ui), false)
;



--DesignArray--
INSERT INTO af.property_config
    (is_required, order_number, creator_id, is_void, tenant_id, property_id, config_property_id, property_ui_id, is_layout_variable)
VALUES
    (true, 6, '1', false, 1, (SELECT id FROM af.property WHERE code = 'randIBD_OFT'), 172, null, false)
;
