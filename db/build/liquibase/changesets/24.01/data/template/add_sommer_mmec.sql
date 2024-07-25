
--liquibase formatted sql

--changeset postgres:add_sommer_analysis_configuration_data context:template splitStatements:false rollbackSplitStatements:false
--comment: BA-778 Add analysis configuration data for sommer mmec engine


-- config_110005.cfg
WITH analysis_config AS (
	INSERT INTO af.property(
		code, "name", "label", description, "type", data_type,"statement"
	) VALUES (
		'config_110005.cfg', 'Scenario 2 - sommer mmec', 
		'Scenario 2 - sommer mmec', 'From course example', 
		'catalog_item', 'character varying','sommer-mmec'
	) RETURNING id
)
INSERT INTO af.property_config(
	order_number, creation_timestamp, creator_id,
	is_void, property_id, config_property_id, is_layout_variable
) VALUES (
	6, 'now()', '1', false, 
	(SELECT id FROM af.property WHERE code = 'analysis_config'), 
	(SELECT id FROM analysis_config), false
);



-- add config_110005 meta data
WITH analysis_config AS (
	SELECT id FROM af.property WHERE code = 'config_110005.cfg' LIMIT 1
)
INSERT INTO af.property_meta(code,value,property_id) VALUES 
	('config_version', '2', (SELECT id FROM analysis_config)),
	('date', '13-Nov-2021', (SELECT id FROM analysis_config)),
	('author', 'Josh L.S.', (SELECT id FROM analysis_config)),
	('email', 'jdl232@cornell.edu', (SELECT id FROM analysis_config)),
	('engine', 'sommer - mmec', (SELECT id FROM analysis_config)),
    ('design',  'RCBD', (SELECT id FROM analysis_config)),
	('trait_level', 'plot', (SELECT id FROM analysis_config)),
    ('analysis_objective', 'prediction', (SELECT id FROM analysis_config)),
    ('exp_analysis_pattern', 'single', (SELECT id FROM analysis_config)),
    ('loc_analysis_pattern', 'single', (SELECT id FROM analysis_config)),
    ('year_analysis_pattern', 'single', (SELECT id FROM analysis_config)),
    ('trait_pattern', 'univariate', (SELECT id FROM analysis_config));


-- add formula to config_110005
WITH config_formula AS (
	INSERT INTO af.property(
		type, data_type, code, "name", "label", "statement"
	) VALUES (
		'catalog_item', 'character varying', 'formula_opt1', 
		'Pheno from loc with variety', 
		'Pheno from loc with variety', 
		'fixed = phenotype~loc, random = ~vsc(isc(variety),Gu=GT)'
	) RETURNING id
),
config_formula_property_config_link AS (
	INSERT INTO af.property_config(
		order_number, creation_timestamp, creator_id,
		is_void, property_id, config_property_id, is_layout_variable
	) VALUES (
		1, 'now()', '1', false,
		(SELECT id FROM af.property WHERE code='formula' LIMIT 1), 
		(SELECT id FROM config_formula), false
	)
),
config_formula_config_110005_link AS (
	INSERT INTO af.property_config(
		order_number, creation_timestamp, creator_id,
		is_void, property_id, config_property_id, is_layout_variable
	) VALUES (
		1, 'now()', '1', false,
		(SELECT id FROM af.property WHERE code = 'config_110005.cfg' LIMIT 1),
		(SELECT id FROM config_formula), false
	)

)
SELECT * FROM config_formula;


-- add residual to config_110005
WITH config_residual AS (
     INSERT INTO af.property(
		type, data_type, code, "name", "label", "statement"
	) VALUES (
		'catalog_item', 'character varying', 'residual_opt1', 
		'Units', 
		'Units', 
		'~ units'
	) RETURNING id
),
config_residual_property_config_link AS (
	INSERT INTO af.property_config(
		order_number, creation_timestamp, creator_id,
		is_void, property_id, config_property_id, is_layout_variable
	) VALUES (
		1, 'now()', '1', false,
		(SELECT id FROM af.property WHERE code='residual' LIMIT 1), 
		(SELECT id FROM config_residual LIMIT 1), false
	)
),
config_residual_config_110005_link AS (
	INSERT INTO af.property_config(
		order_number, creation_timestamp, creator_id,
		is_void, property_id, config_property_id, is_layout_variable
	) VALUES (
		1, 'now()', '1', false,
		(SELECT id FROM af.property WHERE code = 'config_110005.cfg' LIMIT 1),
		(SELECT id FROM config_residual LIMIT 1), false
	)

)
SELECT * FROM config_residual;



WITH config_prediction AS (
	INSERT INTO af.property(
		type, data_type, code, "name", "statement"
	) VALUES (
		'catalog_item', 'character varying', 'Yield', 'Yield', 'YLDPLOT'
	) RETURNING id
),
config_prediction_property_config_link AS (
	INSERT INTO af.property_config(
		order_number, creation_timestamp, creator_id,
		is_void, property_id, config_property_id, is_layout_variable
	) VALUES (
		1, 'now()', '1', false,
		(SELECT id FROM af.property WHERE code='prediction' LIMIT 1) , 
		(SELECT id FROM config_prediction LIMIT 1), false
	)
),
config_prediction_config_110005_link AS (
	INSERT INTO af.property_config(
		order_number, creation_timestamp, creator_id,
		is_void, property_id, config_property_id, is_layout_variable
	) VALUES (
		1, 'now()', '1', false,
		(SELECT id FROM af.property WHERE code = 'config_110005.cfg' LIMIT 1),
		(SELECT id FROM config_prediction LIMIT 1), false
	)

) SELECT * from config_prediction;

-- add trial as stat factor
WITH stat_factor AS (
	INSERT INTO af.property (code, type) VALUES  ('trial', 'catalog_item') RETURNING id
),
stat_factor_config AS (
	INSERT INTO af.property_config (order_number, creation_timestamp, creator_id,is_void, 
		property_id, config_property_id, is_layout_variable
	) VALUES(
		4, 'now()', '1', false,
		(SELECT id FROM af.property WHERE code = 'analysis_module_fields' LIMIT 1),
		(SELECT id FROM stat_factor LIMIT 1), false
	)
), 
stat_factor_meta AS (
	INSERT INTO af.property_meta(code,value,property_id) 
	VALUES(
		'definition', 'trialDbId', (SELECT id FROM stat_factor LIMIT 1)
	)
),
stat_factor_config_110005_link AS (
	INSERT INTO af.property_config (
		order_number, creation_timestamp, creator_id, is_void,property_id, 
		config_property_id, is_layout_variable
	) VALUES (
		5, 'now()', '1', false, 
		(SELECT id FROM af.property WHERE code = 'config_110005.cfg' LIMIT 1),
		(SELECT id FROM stat_factor LIMIT 1), false
	)
)
SELECT id AS stat_factor_id FROM stat_factor LIMIT 1;

-- add plot as stat factor
WITH stat_factor AS (
	INSERT INTO af.property (code, type) VALUES  ('plot', 'catalog_item') RETURNING id
),
stat_factor_config AS (
	INSERT INTO af.property_config (order_number, creation_timestamp, creator_id,is_void, 
		property_id, config_property_id, is_layout_variable
	) VALUES(
		4, 'now()', '1', false,
		(SELECT id FROM af.property WHERE code = 'analysis_module_fields' LIMIT 1),
		(SELECT id FROM stat_factor LIMIT 1), false
	)
), 
stat_factor_meta AS (
	INSERT INTO af.property_meta(code,value,property_id) 
	VALUES(	
		'definition', 'observationUnitDbId', (SELECT id FROM stat_factor)
	)
),
stat_factor_config_110005_link AS (
	INSERT INTO af.property_config (
		order_number, creation_timestamp, creator_id, is_void,property_id, 
		config_property_id, is_layout_variable
	) VALUES (
		5, 'now()', '1', false, 
		(SELECT id FROM af.property WHERE code = 'config_110005.cfg' LIMIT 1),
		(SELECT id FROM stat_factor LIMIT 1), false
	)
)
SELECT id AS stat_factor_id FROM stat_factor;


-- add genotype as stat factor
WITH stat_factor AS (
	INSERT INTO af.property (code, type) VALUES  ('genotype', 'catalog_item') RETURNING id
),
stat_factor_config AS (
	INSERT INTO af.property_config (order_number, creation_timestamp, creator_id,is_void, 
		property_id, config_property_id, is_layout_variable
	) VALUES(
		4, 'now()', '1', false,
		(SELECT id FROM af.property WHERE code = 'analysis_module_fields'),
		(SELECT id FROM stat_factor LIMIT 1), false
	)
), 
stat_factor_meta AS (
	INSERT INTO af.property_meta(code,value,property_id) 
	VALUES(
		'definition', 'germplasmDbId', (SELECT id FROM stat_factor LIMIT 1)
	)
),
stat_factor_config_110005_link AS (
	INSERT INTO af.property_config (
		order_number, creation_timestamp, creator_id, is_void,property_id, 
		config_property_id, is_layout_variable
	) VALUES (
		5, 'now()', '1', false, 
		(SELECT id FROM af.property WHERE code = 'config_110005.cfg' LIMIT 1),
		(SELECT id FROM stat_factor LIMIT 1), false
	)
)
SELECT id AS stat_factor_id FROM stat_factor;


-- add rep as stat factor
WITH stat_factor AS (
	INSERT INTO af.property (code, type) VALUES  ('rep', 'catalog_item') RETURNING id
),
stat_factor_config AS (
	INSERT INTO af.property_config (order_number, creation_timestamp, creator_id,is_void, 
		property_id, config_property_id, is_layout_variable
	) VALUES(
		4, 'now()', '1', false,
		(SELECT id FROM af.property WHERE code = 'analysis_module_fields' LIMIT 1),
		(SELECT id FROM stat_factor LIMIT 1), false
	)
), 
stat_factor_meta AS (
	INSERT INTO af.property_meta(code,value,property_id) 
	VALUES(
		'definition', 'replicate', (SELECT id FROM stat_factor)
	)
),
stat_factor_config_110005_link AS (
	INSERT INTO af.property_config (
		order_number, creation_timestamp, creator_id, is_void,property_id, 
		config_property_id, is_layout_variable
	) VALUES (
		5, 'now()', '1', false, 
		(SELECT id FROM af.property WHERE code = 'config_110005.cfg' LIMIT 1),
		(SELECT id FROM stat_factor LIMIT 1), false
	)
)
SELECT id AS stat_factor_id FROM stat_factor;


-- add loc as stat factor
WITH stat_factor AS (
	INSERT INTO af.property (code, type) VALUES  ('loc', 'catalog_item') RETURNING id
),
stat_factor_config AS (
	INSERT INTO af.property_config (order_number, creation_timestamp, creator_id,is_void, 
		property_id, config_property_id, is_layout_variable
	) VALUES(
		4, 'now()', '1', false,
		(SELECT id FROM af.property WHERE code = 'analysis_module_fields' LIMIT 1),
		(SELECT id FROM stat_factor LIMIT 1), false
	)
), 
stat_factor_meta AS (
	INSERT INTO af.property_meta(code,value,property_id) 
	VALUES(
		'definition', 'locationDbId', (SELECT id FROM stat_factor)
	)
),
stat_factor_config_110005_link AS (
	INSERT INTO af.property_config (
		order_number, creation_timestamp, creator_id, is_void,property_id, 
		config_property_id, is_layout_variable
	) VALUES (
		5, 'now()', '1', false, 
		(SELECT id FROM af.property WHERE code = 'config_110005.cfg' LIMIT 1),
		(SELECT id FROM stat_factor LIMIT 1), false
	)
)
SELECT id AS stat_factor_id FROM stat_factor;


-- add col as stat factor
WITH stat_factor AS (
	INSERT INTO af.property (code, type) VALUES  ('col', 'catalog_item') RETURNING id
),
stat_factor_config AS (
	INSERT INTO af.property_config (order_number, creation_timestamp, creator_id,is_void, 
		property_id, config_property_id, is_layout_variable
	) VALUES(
		4, 'now()', '1', false,
		(SELECT id FROM af.property WHERE code = 'analysis_module_fields' LIMIT 1),
		(SELECT id FROM stat_factor LIMIT 1), false
	)
), 
stat_factor_meta AS (
	INSERT INTO af.property_meta(code,value,property_id) 
	VALUES(
		'definition', 'positionCoordinateX', (SELECT id FROM stat_factor)
	)
),
stat_factor_config_110005_link AS (
	INSERT INTO af.property_config (
		order_number, creation_timestamp, creator_id, is_void,property_id, 
		config_property_id, is_layout_variable
	) VALUES (
		5, 'now()', '1', false, 
		(SELECT id FROM af.property WHERE code = 'config_110005.cfg' LIMIT 1),
		(SELECT id FROM stat_factor LIMIT 1), false
	)
)
SELECT id AS stat_factor_id FROM stat_factor;


-- add row as stat factor
WITH stat_factor AS (
	INSERT INTO af.property (code, type) VALUES  ('row', 'catalog_item') RETURNING id
),
stat_factor_config AS (
	INSERT INTO af.property_config (order_number, creation_timestamp, creator_id,is_void, 
		property_id, config_property_id, is_layout_variable
	) VALUES(
		4, 'now()', '1', false,
		(SELECT id FROM af.property WHERE code = 'analysis_module_fields' LIMIT 1),
		(SELECT id FROM stat_factor LIMIT 1), false
	)
), 
stat_factor_meta AS (
	INSERT INTO af.property_meta(code,value,property_id) 
	VALUES(
		'definition', 'positionCoordinateY', (SELECT id FROM stat_factor LIMIT 1)
	)
),
stat_factor_config_110005_link AS (
	INSERT INTO af.property_config (
		order_number, creation_timestamp, creator_id, is_void,property_id, 
		config_property_id, is_layout_variable
	) VALUES (
		5, 'now()', '1', false, 
		(SELECT id FROM af.property WHERE code = 'config_110005.cfg' LIMIT 1),
		(SELECT id FROM stat_factor LIMIT 1), false
	)
)
SELECT id AS stat_factor_id FROM stat_factor;