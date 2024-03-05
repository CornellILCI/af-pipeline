--liquibase formatted sql

--changeset postgres:add_asreml_r_analysis_configuration_data context:template splitStatements:false rollbackSplitStatements:false
--comment: BA2-44 Add analysis configuration data for Asreml-R engine 20025


-- config_20025.cfg
WITH analysis_config AS (
	INSERT INTO af.property(
		code, "name", "label", description, "type", data_type
	) VALUES (
		'config_20025.cfg', 'Multi-Exp 2-stage analysis - 1st Stage - RCBD & Aug RCBD - fix model - spatial',
		'Multi-Exp 2-stage analysis - 1st Stage - RCBD & Aug RCBD - fix model - spatial', 
		'Executes the first stage of a two stage analysis for RCBD experiments, genotype as fixed and autoregressive for rows and columns as spatial adjustment', 
		'catalog_item', 'character varying'
	) RETURNING id
)
INSERT INTO af.property_config(
	order_number, creation_timestamp, creator_id,
	is_void, property_id, config_property_id, is_layout_variable
) VALUES (
	1, 'now()', '1', false, 
	(SELECT id FROM af.property WHERE code = 'analysis_config'), 
	(SELECT id FROM analysis_config), false
);


-- add loc as stat factor
INSERT INTO af.property_config (
	order_number, creation_timestamp, creator_id, is_void,property_id, 
	config_property_id, is_layout_variable
) VALUES (
	1, 'now()', '1', false, 
	(SELECT id FROM af.property WHERE code = 'config_20025.cfg'),
	(SELECT id FROM af.property WHERE code = 'loc' AND data_type = 'factor'), false
);


-- add expt as stat factor
INSERT INTO af.property_config (
	order_number, creation_timestamp, creator_id, is_void,property_id, 
	config_property_id, is_layout_variable
) VALUES (
	2, 'now()', '1', false, 
	(SELECT id FROM af.property WHERE code = 'config_20025.cfg'),
	(SELECT id FROM af.property WHERE code = 'expt' AND data_type = 'factor'), false
);

-- add germplasm as stat factor
INSERT INTO af.property_config(
	order_number, creation_timestamp, creator_id, is_void,property_id,
	config_property_id, is_layout_variable
) VALUES (
	2, 'now()', '1', false, 
	(SELECT id FROM af.property WHERE code = 'config_20025.cfg'),
	(SELECT id FROM af.property WHERE code = 'ge' AND data_type = 'factor'), false
);

-- add plot as stat factor
INSERT INTO af.property_config (
	order_number, creation_timestamp, creator_id, is_void,property_id, 
	config_property_id, is_layout_variable
) VALUES (
	2, 'now()', '1', false, 
	(SELECT id FROM af.property WHERE code = 'config_20025.cfg'),
	(SELECT id FROM af.property WHERE code = 'plot' AND data_type = 'factor'), false
);

-- add col as stat factor
INSERT INTO af.property_config (
	order_number, creation_timestamp, creator_id, is_void,property_id, 
	config_property_id, is_layout_variable
) VALUES (
	2, 'now()', '1', false, 
	(SELECT id FROM af.property WHERE code = 'config_20025.cfg'),
	(SELECT id FROM af.property WHERE code = 'col' AND data_type = 'factor'), false
);


-- add row as stat factor
INSERT INTO af.property_config (
	order_number, creation_timestamp, creator_id, is_void,property_id, 
	config_property_id, is_layout_variable
) VALUES (
	2, 'now()', '1', false, 
	(SELECT id FROM af.property WHERE code = 'config_20025.cfg'),
	(SELECT id FROM af.property WHERE code = 'row' AND data_type = 'factor'), false
);

-- add rep as stat factor
INSERT INTO af.property_config (
	order_number, creation_timestamp, creator_id, is_void,property_id, 
	config_property_id, is_layout_variable
) VALUES (
	2, 'now()', '1', false, 
	(SELECT id FROM af.property WHERE code = 'config_20025.cfg'),
	(SELECT id FROM af.property WHERE code = 'rep' AND data_type = 'factor'), false
);

-- add config_20025 metadata
WITH analysis_config AS (
	SELECT id FROM af.property WHERE code = 'config_20025.cfg'
)
INSERT INTO af.property_meta(code,value,property_id) VALUES
	('config_version', '1', (SELECT id FROM analysis_config)),
	('date', '11-April-2022', (SELECT id FROM analysis_config)),
	('author', 'Pedro Barbosa', (SELECT id FROM analysis_config)),
	('email', 'p.medeiros@cgiar.org', (SELECT id FROM analysis_config)),
	('engine', 'ASREML-R', (SELECT id FROM analysis_config)),
    	('design',  'RCBD', (SELECT id FROM analysis_config)),
    	('design',  'Augmented-RCB', (SELECT id FROM analysis_config)),
	('trait_level', 'plot', (SELECT id FROM analysis_config)),
    	('analysis_objective', 'prediction', (SELECT id FROM analysis_config)),
    	('exp_analysis_pattern', 'multi', (SELECT id FROM analysis_config)),
    	('loc_analysis_pattern', 'single', (SELECT id FROM analysis_config)),
    	('year_analysis_pattern', 'single', (SELECT id FROM analysis_config)),
    	('trait_pattern', 'univariate', (SELECT id FROM analysis_config));

-- add asreml options to config_20025
SELECT af.add_analysis_config_property(
	'asreml_opt1', 'asreml_opt1', 'asreml_opt1', 
	'na.action = na.method(y = ''include'', x = ''include''),workspace = 128e06', 'asreml_options', 'config_20025.cfg');

-- add formula to config_20025
SELECT af.add_analysis_config_property(
	'formula_opt1', 'Analysis with genotype as fixed - BLUEs. RCBD', 'Analysis with genotype as fixed - BLUEs. RCBD', 
	'fixed = {trait_name} ~ rep + ge', 'formula', 'config_20025.cfg');


-- add residual:Univariate homogeneous variance model to config_20025
SELECT af.add_analysis_config_property(
	'residual_opt1', 'Autoregressive order 1 spatial structure (AR1row x AR1col)', 'Autoregressive order 1 spatial structure (AR1row x AR1col)', 
	'~ ar1(row):ar1(col)', 'residual', 'config_20025.cfg');


-- add prediction to config_20025
SELECT af.add_analysis_config_property('g', 'G', 'G', 'ge', 'prediction', 'config_20025.cfg');




