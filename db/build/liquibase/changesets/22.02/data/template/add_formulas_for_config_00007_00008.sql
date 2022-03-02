--liquibase formatted sql

--changeset postgres:add_formulas_for_config_00007_00008 context:template splitStatements:false rollbackSplitStatements:false
--comment: BA-917 Modify config 0007 and 0008 formula entries

-- add formula to config_00007
WITH config_formula AS (
	INSERT INTO af.property(
		type, data_type, code, "name", "label", "statement"
	) VALUES (
		'catalog_item', 'character varying', 'formula_opt7', 
		'RCBD SEML Univariate - G x E as CORUH', 
		'RCBD SEML Univariate - G x E as CORUH', 
		'{trait_name} ~ mu loc !r coruh(loc).id(entry) idh(loc).rep !f mv'
	) RETURNING id
),
config_formula_property_config_link AS (
	INSERT INTO af.property_config(
		order_number, creation_timestamp, creator_id,
		is_void, property_id, config_property_id, is_layout_variable
	) VALUES (
		1, 'now()', '1', false,
		(SELECT id FROM af.property WHERE code='formula'), 
		(SELECT id FROM config_formula), false
	)
),
config_formula_config_00007_link AS (
	UPDATE af.property_config
    SET config_property_id = (SELECT id FROM config_formula)
    WHERE property_id = (SELECT id FROM af.property WHERE code = 'config_00007.cfg')
    AND config_property_id=149
)
SELECT * FROM config_formula;


-- add formula to config_00008
WITH config_formula AS (
	INSERT INTO af.property(
		type, data_type, code, "name", "label", "statement"
	) VALUES (
		'catalog_item', 'character varying', 'formula_opt8', 
		'Alpha-Lattice MET Univariate - G x E as CORUH', 
		'Alpha-Lattice MET Univariate - G x E as CORUH', 
		'{trait_name} ~ mu loc loc.rep !r idh(loc).rep.block coruh(loc).id(entry) !f mv'
	) RETURNING id
),
config_formula_property_config_link AS (
	INSERT INTO af.property_config(
		order_number, creation_timestamp, creator_id,
		is_void, property_id, config_property_id, is_layout_variable
	) VALUES (
		1, 'now()', '1', false,
		(SELECT id FROM af.property WHERE code='formula'), 
		(SELECT id FROM config_formula), false
	)
),
config_formula_config_00008_link AS (
	UPDATE af.property_config
    SET config_property_id = (SELECT id FROM config_formula)
    WHERE property_id = (SELECT id FROM af.property WHERE code = 'config_00008.cfg')
    AND config_property_id=151
)
SELECT * FROM config_formula;