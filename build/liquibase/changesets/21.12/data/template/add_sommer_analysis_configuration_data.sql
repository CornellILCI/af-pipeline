--liquibase formatted sql

--changeset postgres:add_sommer_analysis_configuration_data context:template splitStatements:false rollbackSplitStatements:false
--comment: BA-778 Add analysis configuration data for sommer engine


-- config_10001.cfg
WITH analysis_config AS (
	INSERT INTO af.property(
		code, "name", "label", description, "type", data_type
	) VALUES (
		'config_10001.cfg', 'RCBD univariate - sommer', 
		'RCBD univariate - sommer', 'RCBD single loc, single year and univariate', 
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


-- config_10002.cfg
WITH analysis_config AS (
	INSERT INTO af.property(
		code, "name", "label", description, "type", data_type
	) VALUES (
		'config_10002.cfg', 'RCBD univariate - GBLUP - sommer', 
		'RCBD univariate - GBLUP - sommer', 'GBLUP for RCBD single loc, univariate', 
		'catalog_item', 'character varying'
	) RETURNING id
)
INSERT INTO af.property_config(
	order_number, creation_timestamp, creator_id,
	is_void, property_id, config_property_id,
	is_layout_variable
) VALUES (
	2, 'now()', '1', false, 
	(SELECT id FROM af.property WHERE code = 'analysis_config'), 
	(SELECT id FROM analysis_config), false
);


-- config_10003.cfg
WITH analysis_config AS (
	INSERT INTO af.property(
		code, "name", "label", description, "type", data_type
	) VALUES (
		'config_10003.cfg', 'RCBD univariate - GBLUP MET US - sommer', 
		'RCBD univariate - GBLUP MET US - sommer', 'GBLUP for RCBD multi loc unstructured model, univariate', 
		'catalog_item','character varying'
	) RETURNING id
)
INSERT INTO af.property_config(
	order_number, creation_timestamp, creator_id, 
	is_void, property_id, config_property_id, is_layout_variable
) VALUES (
	3, 'now()', '1', false, 
	(SELECT id FROM af.property WHERE code = 'analysis_config') , 
	(SELECT id FROM analysis_config), false
);


-- add plot as stat factor
WITH stat_factor AS (
	INSERT INTO af.property (code, type) VALUES  ('plot', 'catalog_item') RETURNING id
),
stat_factor_config AS (
	INSERT INTO af.property_config (order_number, creation_timestamp, creator_id,is_void, 
		property_id, config_property_id, is_layout_variable
	) VALUES(
		4, 'now()', '1', false,
		(SELECT id FROM af.property WHERE code = 'analysis_module_fields'),
		(SELECT id FROM stat_factor), false
	)
), 
stat_factor_meta AS (
	INSERT INTO af.property_meta(code,value,property_id) 
	VALUES(
		'definition', 'observationUnitDbId', (SELECT id FROM stat_factor)
	)
),
stat_factor_config_10001_link AS (
	INSERT INTO af.property_config (
		order_number, creation_timestamp, creator_id, is_void,property_id, 
		config_property_id, is_layout_variable
	) VALUES (
		5, 'now()', '1', false, 
		(SELECT id FROM af.property WHERE code = 'config_10001.cfg'),
		(SELECT id FROM stat_factor), false
	)
),
stat_factor_config_10002_link AS (
	INSERT INTO af.property_config(
		order_number, creation_timestamp, creator_id, is_void,property_id,
		config_property_id, is_layout_variable
	) VALUES (
		6, 'now()', '1', false, 
		(SELECT id FROM af.property WHERE code = 'config_10002.cfg'),
		(SELECT id FROM stat_factor), false
	)
),
stat_factor_config_10003_link AS (
	INSERT INTO af.property_config(
		order_number, creation_timestamp, creator_id,
		is_void, property_id, config_property_id, 
		is_layout_variable
	) VALUES (
		7, 'now()', '1', false, 
		(SELECT id FROM af.property WHERE code = 'config_10003.cfg'),
		(SELECT id FROM stat_factor), false
	)
)
SELECT id AS stat_factor_id FROM stat_factor;


-- add ID as stat factor
WITH stat_factor AS (
	INSERT INTO af.property (code, type) VALUES  ('ID', 'catalog_item') RETURNING id
),
stat_factor_config AS (
	INSERT INTO af.property_config (order_number, creation_timestamp, creator_id,is_void, 
		property_id, config_property_id, is_layout_variable
	) VALUES(
		4, 'now()', '1', false,
		(SELECT id FROM af.property WHERE code = 'analysis_module_fields'),
		(SELECT id FROM stat_factor), false
	)
), 
stat_factor_meta AS (
	INSERT INTO af.property_meta(code,value,property_id) 
	VALUES(
		'definition', 'germplasmDbId', (SELECT id FROM stat_factor)
	)
),
stat_factor_config_10001_link AS (
	INSERT INTO af.property_config (
		order_number, creation_timestamp, creator_id, is_void,property_id, 
		config_property_id, is_layout_variable
	) VALUES (
		5, 'now()', '1', false, 
		(SELECT id FROM af.property WHERE code = 'config_10001.cfg'),
		(SELECT id FROM stat_factor), false
	)
),
stat_factor_config_10002_link AS (
	INSERT INTO af.property_config(
		order_number, creation_timestamp, creator_id, is_void,property_id,
		config_property_id, is_layout_variable
	) VALUES (
		6, 'now()', '1', false, 
		(SELECT id FROM af.property WHERE code = 'config_10002.cfg'),
		(SELECT id FROM stat_factor), false
	)
),
stat_factor_config_10003_link AS (
	INSERT INTO af.property_config(
		order_number, creation_timestamp, creator_id,
		is_void, property_id, config_property_id, 
		is_layout_variable
	) VALUES (
		7, 'now()', '1', false, 
		(SELECT id FROM af.property WHERE code = 'config_10003.cfg'),
		(SELECT id FROM stat_factor), false
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
		(SELECT id FROM af.property WHERE code = 'analysis_module_fields'),
		(SELECT id FROM stat_factor), false
	)
), 
stat_factor_meta AS (
	INSERT INTO af.property_meta(code,value,property_id) 
	VALUES(
		'definition', 'replicate', (SELECT id FROM stat_factor)
	)
),
stat_factor_config_10001_link AS (
	INSERT INTO af.property_config (
		order_number, creation_timestamp, creator_id, is_void,property_id, 
		config_property_id, is_layout_variable
	) VALUES (
		5, 'now()', '1', false, 
		(SELECT id FROM af.property WHERE code = 'config_10001.cfg'),
		(SELECT id FROM stat_factor), false
	)
),
stat_factor_config_10002_link AS (
	INSERT INTO af.property_config(
		order_number, creation_timestamp, creator_id, is_void,property_id,
		config_property_id, is_layout_variable
	) VALUES (
		6, 'now()', '1', false, 
		(SELECT id FROM af.property WHERE code = 'config_10002.cfg'),
		(SELECT id FROM stat_factor), false
	)
),
stat_factor_config_10003_link AS (
	INSERT INTO af.property_config(
		order_number, creation_timestamp, creator_id,
		is_void, property_id, config_property_id, 
		is_layout_variable
	) VALUES (
		7, 'now()', '1', false, 
		(SELECT id FROM af.property WHERE code = 'config_10003.cfg'),
		(SELECT id FROM stat_factor), false
	)
)
SELECT id AS stat_factor_id FROM stat_factor;


-- add rep as stat factor
-- insert rep as property

WITH stat_factor AS (
	INSERT INTO af.property (code, type) VALUES  ('loc', 'catalog_item') RETURNING id
),
stat_factor_config AS (
	INSERT INTO af.property_config (order_number, creation_timestamp, creator_id,is_void, 
		property_id, config_property_id, is_layout_variable
	) VALUES(
		4, 'now()', '1', false,
		(SELECT id FROM af.property WHERE code = 'analysis_module_fields'),
		(SELECT id FROM stat_factor), false
	)
), 
stat_factor_meta AS (
	INSERT INTO af.property_meta(code,value,property_id) 
	VALUES(
		'definition', 'locationDbId', (SELECT id FROM stat_factor)
	)
),
stat_factor_config_10003_link AS (
	INSERT INTO af.property_config(
		order_number, creation_timestamp, creator_id,
		is_void, property_id, config_property_id, 
		is_layout_variable
	) VALUES (
		7, 'now()', '1', false, 
		(SELECT id FROM af.property WHERE code = 'config_10003.cfg'),
		(SELECT id FROM stat_factor), false
	)
)
SELECT id AS stat_factor_id FROM stat_factor;


-- add config_10001 meta data
WITH analysis_config AS (
	SELECT id FROM af.property WHERE code = 'config_10001.cfg'
)
INSERT INTO af.property_meta(code,value,property_id) VALUES
	('config_version', '2', (SELECT id FROM analysis_config)),
	('date', '13-Nov-2021', (SELECT id FROM analysis_config)),
	('author', 'Pedro Barbosa', (SELECT id FROM analysis_config)),
	('email', 'p.medeiros@cgiar.org', (SELECT id FROM analysis_config)),
	('engine', 'R - sommer', (SELECT id FROM analysis_config)),
    	('design',  'RCBD', (SELECT id FROM analysis_config)),
	('trait_level', 'plot', (SELECT id FROM analysis_config)),
    	('analysis_objective', 'prediction', (SELECT id FROM analysis_config)),
    	('exp_analysis_pattern', 'single', (SELECT id FROM analysis_config)),
    	('loc_analysis_pattern', 'single', (SELECT id FROM analysis_config)),
    	('year_analysis_pattern', 'single', (SELECT id FROM analysis_config)),
    	('trait_pattern', 'univariate', (SELECT id FROM analysis_config));

-- add config_10002 meta data
WITH analysis_config AS (
	SELECT id FROM af.property WHERE code = 'config_10002.cfg'
)
INSERT INTO af.property_meta(code,value,property_id) VALUES
	('config_version', '2', (SELECT id FROM analysis_config)),
	('date', '13-Nov-2021', (SELECT id FROM analysis_config)),
	('author', 'Pedro Barbosa', (SELECT id FROM analysis_config)),
	('email', 'p.medeiros@cgiar.org', (SELECT id FROM analysis_config)),
	('engine', 'R - sommer', (SELECT id FROM analysis_config)),
    	('design',  'RCBD', (SELECT id FROM analysis_config)),
	('trait_level', 'plot', (SELECT id FROM analysis_config)),
    	('analysis_objective', 'prediction', (SELECT id FROM analysis_config)),
    	('exp_analysis_pattern', 'single', (SELECT id FROM analysis_config)),
    	('loc_analysis_pattern', 'single', (SELECT id FROM analysis_config)),
    	('year_analysis_pattern', 'single', (SELECT id FROM analysis_config)),
    	('trait_pattern', 'univariate', (SELECT id FROM analysis_config));

-- add config_10003 meta data
WITH analysis_config AS (
	SELECT id FROM af.property WHERE code = 'config_10003.cfg'
)
INSERT INTO af.property_meta(code,value,property_id) VALUES
	('config_version', '2', (SELECT id FROM analysis_config)),
	('date', '13-Nov-2021', (SELECT id FROM analysis_config)),
	('author', 'Pedro Barbosa', (SELECT id FROM analysis_config)),
	('email', 'p.medeiros@cgiar.org', (SELECT id FROM analysis_config)),
	('engine', 'R - sommer', (SELECT id FROM analysis_config)),
    	('design',  'RCBD', (SELECT id FROM analysis_config)),
	('trait_level', 'plot', (SELECT id FROM analysis_config)),
    	('analysis_objective', 'prediction', (SELECT id FROM analysis_config)),
    	('exp_analysis_pattern', 'single', (SELECT id FROM analysis_config)),
    	('loc_analysis_pattern', 'multi', (SELECT id FROM analysis_config)),
    	('year_analysis_pattern', 'single', (SELECT id FROM analysis_config)),
    	('trait_pattern', 'univariate', (SELECT id FROM analysis_config));


-- add sommer options
WITH sommer_options AS (
	INSERT INTO af.property(
		code, "name", "label", description, "type", data_type
	) VALUES (
		'sommer_options', 'SOMMER Options', 'SOMMER Options',
		'SOMMER Options', 'catalog_root', 'character varying'
	) RETURNING id
)
INSERT INTO af.property_config(
	order_number, creation_timestamp, creator_id, is_void, 
	property_id, config_property_id, is_layout_variable
) VALUES (
	7, 'now()', '1', false, 
	(SELECT id FROM sommer_options), 
	(SELECT id FROM sommer_options), false
);


-- add formula to config_10001
WITH config_formula AS (
	INSERT INTO af.property(
		type, data_type, code, "name", "label", "statement"
	) VALUES (
		'catalog_item', 'character varying', 'formula_opt1', 
		'Univariate. Replicate as fixed and genotype as random effect', 
		'Univariate. Replicate as fixed and genotype as random effect', 
		'fixed = {trait_name} ~ rep, random = ~ ID'
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
config_formula_config_10001_link AS (
	INSERT INTO af.property_config(
		order_number, creation_timestamp, creator_id,
		is_void, property_id, config_property_id, is_layout_variable
	) VALUES (
		1, 'now()', '1', false,
		(SELECT id FROM af.property WHERE code = 'config_10001.cfg'),
		(SELECT id FROM config_formula), false
	)

)
SELECT * FROM config_formula;


-- add formula to config_10002
WITH config_formula AS (
	INSERT INTO af.property(
		type, data_type, code, "name", "label", "statement"
	) VALUES (
		'catalog_item', 'character varying', 'formula_opt2', 
		'GBLUP univariate. Replicate as fixed effect.', 
		'GBLUP univariate. Replicate as fixed effect.', 
		'fixed = {trait_name} ~ rep, random = ~ vs(ID, Gu=A)'
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
config_formula_config_10002_link AS (
	INSERT INTO af.property_config(
		order_number, creation_timestamp, creator_id,
		is_void, property_id, config_property_id, is_layout_variable
	) VALUES (
		1, 'now()', '1', false,
		(SELECT id FROM af.property WHERE code = 'config_10002.cfg'),
		(SELECT id FROM config_formula), false
	)

)
SELECT * FROM config_formula;


-- add formula to config_10003
WITH config_formula AS (
	INSERT INTO af.property(
		type, data_type, code, "name", "label", "statement"
	) VALUES (
		'catalog_item', 'character varying', 'formula_opt3', 
		'GBLUP univariate. MET unstructured model. Environment and Replicate as fixed effect.', 
		'GBLUP univariate. MET unstructured model. Environment and Replicate as fixed effect.', 
		'fixed = {trait_name} ~ loc + loc:rep, random = ~ vs(us(loc),Name, Gu=A)'
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
config_formula_config_10003_link AS (
	INSERT INTO af.property_config(
		order_number, creation_timestamp, creator_id,
		is_void, property_id, config_property_id, is_layout_variable
	) VALUES (
		1, 'now()', '1', false,
		(SELECT id FROM af.property WHERE code = 'config_10003.cfg'),
		(SELECT id FROM config_formula), false
	)

)
SELECT * FROM config_formula;


-- add residual to config_10001, config_10002
WITH config_residual AS (
	INSERT INTO af.property(
		type, data_type, code, "name", "label", "statement"
	) VALUES (
		'catalog_item', 'character varying', 'residual_opt1', 
		'Univariate homogeneous variance model', 
		'Univariate homogeneous variance model', 
		'~ units'
	) RETURNING id
),
config_residual_property_config_link AS (
	INSERT INTO af.property_config(
		order_number, creation_timestamp, creator_id,
		is_void, property_id, config_property_id, is_layout_variable
	) VALUES (
		1, 'now()', '1', false,
		(SELECT id FROM af.property WHERE code='residual'), 
		(SELECT id FROM config_residual), false
	)
),
config_residual_config_10001_link AS (
	INSERT INTO af.property_config(
		order_number, creation_timestamp, creator_id,
		is_void, property_id, config_property_id, is_layout_variable
	) VALUES (
		1, 'now()', '1', false,
		(SELECT id FROM af.property WHERE code = 'config_10001.cfg'),
		(SELECT id FROM config_residual), false
	)

),
config_residual_config_10002_link AS (
	INSERT INTO af.property_config(
		order_number, creation_timestamp, creator_id,
		is_void, property_id, config_property_id, is_layout_variable
	) VALUES (
		1, 'now()', '1', false,
		(SELECT id FROM af.property WHERE code = 'config_10002.cfg'),
		(SELECT id FROM config_residual), false
	)

)
SELECT * FROM config_residual;


-- add residual to config_10003
WITH config_residual AS (
	INSERT INTO af.property(
		type, data_type, code, "name", "label", "statement"
	) VALUES (
		'catalog_item', 'character varying', 'residual_opt3', 
		'Heterogeneous variance in univariate model', 
		'Heterogeneous variance in univariate model', 
		'vs(ds(loc),units),'
	) RETURNING id
),
config_residual_property_config_link AS (
	INSERT INTO af.property_config(
		order_number, creation_timestamp, creator_id,
		is_void, property_id, config_property_id, is_layout_variable
	) VALUES (
		1, 'now()', '1', false,
		(SELECT id FROM af.property WHERE code='residual'), 
		(SELECT id FROM config_residual), false
	)
),
config_residual_config_10003_link AS (
	INSERT INTO af.property_config(
		order_number, creation_timestamp, creator_id,
		is_void, property_id, config_property_id, is_layout_variable
	) VALUES (
		1, 'now()', '1', false,
		(SELECT id FROM af.property WHERE code = 'config_10003.cfg'),
		(SELECT id FROM config_residual), false
	)

)
SELECT * FROM config_residual;


-- add prediction to config_10001, config_10002
WITH config_prediction AS (
	INSERT INTO af.property(
		type, data_type, code, "name", "statement"
	) VALUES (
		'catalog_item', 'character varying', 'g', 'G', 'ID'
	) RETURNING id
),
config_prediction_property_config_link AS (
	INSERT INTO af.property_config(
		order_number, creation_timestamp, creator_id,
		is_void, property_id, config_property_id, is_layout_variable
	) VALUES (
		1, 'now()', '1', false,
		(SELECT id FROM af.property WHERE code='prediction'), 
		(SELECT id FROM config_prediction), false
	)
),
config_prediction_config_10001_link AS (
	INSERT INTO af.property_config(
		order_number, creation_timestamp, creator_id,
		is_void, property_id, config_property_id, is_layout_variable
	) VALUES (
		1, 'now()', '1', false,
		(SELECT id FROM af.property WHERE code = 'config_10001.cfg'),
		(SELECT id FROM config_prediction), false
	)

),
config_prediction_config_10002_link AS (
	INSERT INTO af.property_config(
		order_number, creation_timestamp, creator_id,
		is_void, property_id, config_property_id, is_layout_variable
	) VALUES (
		1, 'now()', '1', false,
		(SELECT id FROM af.property WHERE code = 'config_10002.cfg'),
		(SELECT id FROM config_prediction), false
	)

)
SELECT * FROM config_prediction;


-- add prediction to config_10003
WITH config_prediction AS (
	INSERT INTO af.property(
		type, data_type, code, "name", "statement"
	) VALUES (
		'catalog_item', 'character varying', 'gxe', 'GxE', 'loc.ID'
	) RETURNING id
),
config_prediction_property_config_link AS (
	INSERT INTO af.property_config(
		order_number, creation_timestamp, creator_id,
		is_void, property_id, config_property_id, is_layout_variable
	) VALUES (
		1, 'now()', '1', false,
		(SELECT id FROM af.property WHERE code='prediction'), 
		(SELECT id FROM config_prediction), false
	)
),
config_prediction_config_10003_link AS (
	INSERT INTO af.property_config(
		order_number, creation_timestamp, creator_id,
		is_void, property_id, config_property_id, is_layout_variable
	) VALUES (
		1, 'now()', '1', false,
		(SELECT id FROM af.property WHERE code = 'config_10003.cfg'),
		(SELECT id FROM config_prediction), false
	)

)
SELECT * FROM config_prediction;
