--liquibase formatted sql

--changeset postgres:add_asreml_r_analysis_configuration_data context:template splitStatements:false rollbackSplitStatements:false
--comment: BA-1066 Add analysis configuration data for Asreml-R engine


-- config_20001.cfg
WITH analysis_config AS (
	INSERT INTO af.property(
		code, "name", "label", description, "type", data_type
	) VALUES (
		'config_20001.cfg', 'RCBD univariate - Asreml-R',
		'RCBD univariate - Asreml-R', 
		'RCBD single loc, single year and univariate', 
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


-- config_20020.cfg
WITH analysis_config AS (
	INSERT INTO af.property(
		code, "name", "label", description, "type", data_type
	) VALUES (
		'config_20020.cfg',
		'Multi-Experiment G-Blups. Univariate - Asreml-R', 
		'Multi-Experiment G-Blups. Univariate - Asreml-R', 
		'G-blup for multi experiment, single loc, single year and univariate.',
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


-- config_20020.cfg
WITH analysis_config AS (
	INSERT INTO af.property(
		code, "name", "label", description, "type", data_type
	) VALUES (
		'config_20021.cfg', 'Multi-Experiment, Univariate - Asreml-R',
		'Multi-Experiment, Univariate - Asreml-R', 
		'Blups for genotypes. Multi Experiment, Single loc, univariate',  
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


-- add loc as stat factor
WITH stat_factor AS (
	INSERT INTO af.property (code, type, data_type) VALUES  ('loc', 'catalog_item', 'factor') RETURNING id
),
stat_factor_config AS (
	INSERT INTO af.property_config (order_number, creation_timestamp, creator_id,is_void, 
		property_id, config_property_id, is_layout_variable
	) VALUES(
		1, 'now()', '1', false,
		(SELECT id FROM af.property WHERE code = 'analysis_module_fields'),
		(SELECT id FROM stat_factor), false
	)
), 
stat_factor_meta AS (
	INSERT INTO af.property_meta(code,value,property_id) 
	VALUES(
		'definition', 'loc_id', (SELECT id FROM stat_factor)
	)
),
stat_factor_config_20001_link AS (
	INSERT INTO af.property_config (
		order_number, creation_timestamp, creator_id, is_void,property_id, 
		config_property_id, is_layout_variable
	) VALUES (
		1, 'now()', '1', false, 
		(SELECT id FROM af.property WHERE code = 'config_20001.cfg'),
		(SELECT id FROM stat_factor), false
	)
),
stat_factor_config_20020_link AS (
	INSERT INTO af.property_config(
		order_number, creation_timestamp, creator_id, is_void,property_id,
		config_property_id, is_layout_variable
	) VALUES (
		1, 'now()', '1', false, 
		(SELECT id FROM af.property WHERE code = 'config_20020.cfg'),
		(SELECT id FROM stat_factor), false
	)
),
stat_factor_config_20021_link AS (
	INSERT INTO af.property_config(
		order_number, creation_timestamp, creator_id,
		is_void, property_id, config_property_id, 
		is_layout_variable
	) VALUES (
		1, 'now()', '1', false, 
		(SELECT id FROM af.property WHERE code = 'config_20021.cfg'),
		(SELECT id FROM stat_factor), false
	)
)
SELECT id AS stat_factor_id FROM stat_factor;


-- add expt as stat factor
WITH stat_factor AS (
	INSERT INTO af.property (code, type, data_type) VALUES  ('expt', 'catalog_item', 'factor') RETURNING id
),
stat_factor_config AS (
	INSERT INTO af.property_config (order_number, creation_timestamp, creator_id,is_void, 
		property_id, config_property_id, is_layout_variable
	) VALUES(
		2, 'now()', '1', false,
		(SELECT id FROM af.property WHERE code = 'analysis_module_fields'),
		(SELECT id FROM stat_factor), false
	)
), 
stat_factor_meta AS (
	INSERT INTO af.property_meta(code,value,property_id) 
	VALUES(
		'definition', 'expt_id', (SELECT id FROM stat_factor)
	)
),
stat_factor_config_20001_link AS (
	INSERT INTO af.property_config (
		order_number, creation_timestamp, creator_id, is_void,property_id, 
		config_property_id, is_layout_variable
	) VALUES (
		2, 'now()', '1', false, 
		(SELECT id FROM af.property WHERE code = 'config_20001.cfg'),
		(SELECT id FROM stat_factor), false
	)
),
stat_factor_config_20020_link AS (
	INSERT INTO af.property_config(
		order_number, creation_timestamp, creator_id, is_void,property_id,
		config_property_id, is_layout_variable
	) VALUES (
		2, 'now()', '1', false, 
		(SELECT id FROM af.property WHERE code = 'config_20020.cfg'),
		(SELECT id FROM stat_factor), false
	)
),
stat_factor_config_20021_link AS (
	INSERT INTO af.property_config(
		order_number, creation_timestamp, creator_id,
		is_void, property_id, config_property_id, 
		is_layout_variable
	) VALUES (
		2, 'now()', '1', false, 
		(SELECT id FROM af.property WHERE code = 'config_20021.cfg'),
		(SELECT id FROM stat_factor), false
	)
)
SELECT id AS stat_factor_id FROM stat_factor;


-- add entry as stat factor
WITH stat_factor AS (
	INSERT INTO af.property (code, type, data_type) VALUES  ('entry', 'catalog_item', 'factor') RETURNING id
),
stat_factor_config AS (
	INSERT INTO af.property_config (order_number, creation_timestamp, creator_id,is_void, 
		property_id, config_property_id, is_layout_variable
	) VALUES(
		2, 'now()', '1', false,
		(SELECT id FROM af.property WHERE code = 'analysis_module_fields'),
		(SELECT id FROM stat_factor), false
	)
), 
stat_factor_meta AS (
	INSERT INTO af.property_meta(code,value,property_id) 
	VALUES(
		'definition', 'entry_id', (SELECT id FROM stat_factor)
	)
),
stat_factor_config_20001_link AS (
	INSERT INTO af.property_config (
		order_number, creation_timestamp, creator_id, is_void,property_id, 
		config_property_id, is_layout_variable
	) VALUES (
		2, 'now()', '1', false, 
		(SELECT id FROM af.property WHERE code = 'config_20001.cfg'),
		(SELECT id FROM stat_factor), false
	)
)
SELECT id AS stat_factor_id FROM stat_factor;


-- add germplasm as stat factor
WITH stat_factor AS (
	INSERT INTO af.property (code, type, data_type) VALUES  ('ge', 'catalog_item', 'factor') RETURNING id
),
stat_factor_config AS (
	INSERT INTO af.property_config (order_number, creation_timestamp, creator_id,is_void, 
		property_id, config_property_id, is_layout_variable
	) VALUES(
		2, 'now()', '1', false,
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
stat_factor_config_20020_link AS (
	INSERT INTO af.property_config(
		order_number, creation_timestamp, creator_id, is_void,property_id,
		config_property_id, is_layout_variable
	) VALUES (
		2, 'now()', '1', false, 
		(SELECT id FROM af.property WHERE code = 'config_20020.cfg'),
		(SELECT id FROM stat_factor), false
	)
),
stat_factor_config_20021_link AS (
	INSERT INTO af.property_config(
		order_number, creation_timestamp, creator_id,
		is_void, property_id, config_property_id, 
		is_layout_variable
	) VALUES (
		2, 'now()', '1', false, 
		(SELECT id FROM af.property WHERE code = 'config_20021.cfg'),
		(SELECT id FROM stat_factor), false
	)
)
SELECT id AS stat_factor_id FROM stat_factor;

-- add plot as stat factor
WITH stat_factor AS (
	INSERT INTO af.property (code, type, data_type) VALUES  ('plot', 'catalog_item', 'factor') RETURNING id
),
stat_factor_config AS (
	INSERT INTO af.property_config (order_number, creation_timestamp, creator_id,is_void, 
		property_id, config_property_id, is_layout_variable
	) VALUES(
		2, 'now()', '1', false,
		(SELECT id FROM af.property WHERE code = 'analysis_module_fields'),
		(SELECT id FROM stat_factor), false
	)
), 
stat_factor_meta AS (
	INSERT INTO af.property_meta(code,value,property_id) 
	VALUES(
		'definition', 'plot_id', (SELECT id FROM stat_factor)
	)
),
stat_factor_config_20001_link AS (
	INSERT INTO af.property_config (
		order_number, creation_timestamp, creator_id, is_void,property_id, 
		config_property_id, is_layout_variable
	) VALUES (
		2, 'now()', '1', false, 
		(SELECT id FROM af.property WHERE code = 'config_20001.cfg'),
		(SELECT id FROM stat_factor), false
	)
),
stat_factor_config_20020_link AS (
	INSERT INTO af.property_config(
		order_number, creation_timestamp, creator_id, is_void,property_id,
		config_property_id, is_layout_variable
	) VALUES (
		2, 'now()', '1', false, 
		(SELECT id FROM af.property WHERE code = 'config_20020.cfg'),
		(SELECT id FROM stat_factor), false
	)
),
stat_factor_config_20021_link AS (
	INSERT INTO af.property_config(
		order_number, creation_timestamp, creator_id,
		is_void, property_id, config_property_id, 
		is_layout_variable
	) VALUES (
		2, 'now()', '1', false, 
		(SELECT id FROM af.property WHERE code = 'config_20021.cfg'),
		(SELECT id FROM stat_factor), false
	)
)
SELECT id AS stat_factor_id FROM stat_factor;

-- add col as stat factor
WITH stat_factor AS (
	INSERT INTO af.property (code, type, data_type) VALUES  ('col', 'catalog_item', 'factor') RETURNING id
),
stat_factor_config AS (
	INSERT INTO af.property_config (order_number, creation_timestamp, creator_id,is_void, 
		property_id, config_property_id, is_layout_variable
	) VALUES(
		2, 'now()', '1', false,
		(SELECT id FROM af.property WHERE code = 'analysis_module_fields'),
		(SELECT id FROM stat_factor), false
	)
), 
stat_factor_meta AS (
	INSERT INTO af.property_meta(code,value,property_id) 
	VALUES(
		'definition', 'pa_x', (SELECT id FROM stat_factor)
	)
),
stat_factor_config_20001_link AS (
	INSERT INTO af.property_config (
		order_number, creation_timestamp, creator_id, is_void,property_id, 
		config_property_id, is_layout_variable
	) VALUES (
		2, 'now()', '1', false, 
		(SELECT id FROM af.property WHERE code = 'config_20001.cfg'),
		(SELECT id FROM stat_factor), false
	)
),
stat_factor_config_20020_link AS (
	INSERT INTO af.property_config(
		order_number, creation_timestamp, creator_id, is_void,property_id,
		config_property_id, is_layout_variable
	) VALUES (
		2, 'now()', '1', false, 
		(SELECT id FROM af.property WHERE code = 'config_20020.cfg'),
		(SELECT id FROM stat_factor), false
	)
),
stat_factor_config_20021_link AS (
	INSERT INTO af.property_config(
		order_number, creation_timestamp, creator_id,
		is_void, property_id, config_property_id, 
		is_layout_variable
	) VALUES (
		2, 'now()', '1', false, 
		(SELECT id FROM af.property WHERE code = 'config_20021.cfg'),
		(SELECT id FROM stat_factor), false
	)
)
SELECT id AS stat_factor_id FROM stat_factor;

-- add row as stat factor
WITH stat_factor AS (
	INSERT INTO af.property (code, type, data_type) VALUES  ('row', 'catalog_item', 'factor') RETURNING id
),
stat_factor_config AS (
	INSERT INTO af.property_config (order_number, creation_timestamp, creator_id,is_void, 
		property_id, config_property_id, is_layout_variable
	) VALUES(
		2, 'now()', '1', false,
		(SELECT id FROM af.property WHERE code = 'analysis_module_fields'),
		(SELECT id FROM stat_factor), false
	)
), 
stat_factor_meta AS (
	INSERT INTO af.property_meta(code,value,property_id) 
	VALUES(
		'definition', 'pa_y', (SELECT id FROM stat_factor)
	)
),
stat_factor_config_20001_link AS (
	INSERT INTO af.property_config (
		order_number, creation_timestamp, creator_id, is_void,property_id, 
		config_property_id, is_layout_variable
	) VALUES (
		2, 'now()', '1', false, 
		(SELECT id FROM af.property WHERE code = 'config_20001.cfg'),
		(SELECT id FROM stat_factor), false
	)
),
stat_factor_config_20020_link AS (
	INSERT INTO af.property_config(
		order_number, creation_timestamp, creator_id, is_void,property_id,
		config_property_id, is_layout_variable
	) VALUES (
		2, 'now()', '1', false, 
		(SELECT id FROM af.property WHERE code = 'config_20020.cfg'),
		(SELECT id FROM stat_factor), false
	)
),
stat_factor_config_20021_link AS (
	INSERT INTO af.property_config(
		order_number, creation_timestamp, creator_id,
		is_void, property_id, config_property_id, 
		is_layout_variable
	) VALUES (
		2, 'now()', '1', false, 
		(SELECT id FROM af.property WHERE code = 'config_20021.cfg'),
		(SELECT id FROM stat_factor), false
	)
)
SELECT id AS stat_factor_id FROM stat_factor;


-- add rep as stat factor
WITH stat_factor AS (
	INSERT INTO af.property (code, type, data_type) VALUES  ('rep', 'catalog_item', 'factor') RETURNING id
),
stat_factor_config AS (
	INSERT INTO af.property_config (order_number, creation_timestamp, creator_id,is_void, 
		property_id, config_property_id, is_layout_variable
	) VALUES(
		2, 'now()', '1', false,
		(SELECT id FROM af.property WHERE code = 'analysis_module_fields'),
		(SELECT id FROM stat_factor), false
	)
), 
stat_factor_meta AS (
	INSERT INTO af.property_meta(code,value,property_id) 
	VALUES(
		'definition', 'rep_factor', (SELECT id FROM stat_factor)
	)
),
stat_factor_config_20001_link AS (
	INSERT INTO af.property_config (
		order_number, creation_timestamp, creator_id, is_void,property_id, 
		config_property_id, is_layout_variable
	) VALUES (
		2, 'now()', '1', false, 
		(SELECT id FROM af.property WHERE code = 'config_20001.cfg'),
		(SELECT id FROM stat_factor), false
	)
),
stat_factor_config_20020_link AS (
	INSERT INTO af.property_config(
		order_number, creation_timestamp, creator_id, is_void,property_id,
		config_property_id, is_layout_variable
	) VALUES (
		2, 'now()', '1', false, 
		(SELECT id FROM af.property WHERE code = 'config_20020.cfg'),
		(SELECT id FROM stat_factor), false
	)
),
stat_factor_config_20021_link AS (
	INSERT INTO af.property_config(
		order_number, creation_timestamp, creator_id,
		is_void, property_id, config_property_id, 
		is_layout_variable
	) VALUES (
		2, 'now()', '1', false, 
		(SELECT id FROM af.property WHERE code = 'config_20021.cfg'),
		(SELECT id FROM stat_factor), false
	)
)
SELECT id AS stat_factor_id FROM stat_factor;

-- add config_20001 meta data
WITH analysis_config AS (
	SELECT id FROM af.property WHERE code = 'config_20001.cfg'
)
INSERT INTO af.property_meta(code,value,property_id) VALUES
	('config_version', '1', (SELECT id FROM analysis_config)),
	('date', '08-March-2022', (SELECT id FROM analysis_config)),
	('author', 'Pedro Barbosa', (SELECT id FROM analysis_config)),
	('email', 'p.medeiros@cgiar.org', (SELECT id FROM analysis_config)),
	('engine', 'ASREML-R', (SELECT id FROM analysis_config)),
    	('design',  'RCBD', (SELECT id FROM analysis_config)),
    	('design',  'Augmented-RCB', (SELECT id FROM analysis_config)),
	('trait_level', 'plot', (SELECT id FROM analysis_config)),
    	('analysis_objective', 'prediction', (SELECT id FROM analysis_config)),
    	('exp_analysis_pattern', 'single', (SELECT id FROM analysis_config)),
    	('loc_analysis_pattern', 'single', (SELECT id FROM analysis_config)),
    	('year_analysis_pattern', 'single', (SELECT id FROM analysis_config)),
    	('trait_pattern', 'univariate', (SELECT id FROM analysis_config));


-- add config_20020 meta data
WITH analysis_config AS (
	SELECT id FROM af.property WHERE code = 'config_20020.cfg'
)
INSERT INTO af.property_meta(code,value,property_id) VALUES
	('config_version', '1', (SELECT id FROM analysis_config)),
	('date', '08-March-2022', (SELECT id FROM analysis_config)),
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


-- add config_20021 meta data
WITH analysis_config AS (
	SELECT id FROM af.property WHERE code = 'config_20021.cfg'
)
INSERT INTO af.property_meta(code,value,property_id) VALUES
	('config_version', '1', (SELECT id FROM analysis_config)),
	('date', '08-March-2022', (SELECT id FROM analysis_config)),
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


-- add formula to config_20001
WITH config_formula AS (
	INSERT INTO af.property(
		type, data_type, code, "name", "label", "statement"
	) VALUES (
		'catalog_item', 'character varying', 'formula_opt1', 
		'Univariate. Replicate as fixed and genotype as random effect', 
		'Univariate. Replicate as fixed and genotype as random effect', 
		'fixed = {trait_name} ~ rep, random = ~ entry'
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
		(SELECT id FROM af.property WHERE code = 'config_20001.cfg'),
		(SELECT id FROM config_formula), false
	)

)
SELECT * FROM config_formula;

-- add formula to config_20020
WITH config_formula AS (
	INSERT INTO af.property(
		type, data_type, code, "name", "label", "statement"
	) VALUES (
		'catalog_item', 'character varying', 'formula_opt1', 
		'Univariate. G-blup', 
		'Univariate. G-blup', 
		'fixed = {trait_name} ~ at(expt):rep, random = ~ vm(ge, Ginv)'
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
		(SELECT id FROM af.property WHERE code = 'config_20020.cfg'),
		(SELECT id FROM config_formula), false
	)

)
SELECT * FROM config_formula;


-- add formula to config_20021
WITH config_formula AS (
	INSERT INTO af.property(
		type, data_type, code, "name", "label", "statement"
	) VALUES (
		'catalog_item', 'character varying', 'formula_opt1', 
		'Genotype as random. Reps within experiments.', 
		'Genotype as random. Reps within experiments.', 
		'fixed = {trait_name} ~ at(expt):rep, random = ~ ge'
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
		(SELECT id FROM af.property WHERE code = 'config_20021.cfg'),
		(SELECT id FROM config_formula), false
	)

)
SELECT * FROM config_formula;


-- add residual:Univariate homogeneous variance model to config_20001, config_20020, config_20021
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
config_residual_config_20001_link AS (
	INSERT INTO af.property_config(
		order_number, creation_timestamp, creator_id,
		is_void, property_id, config_property_id, is_layout_variable
	) VALUES (
		1, 'now()', '1', false,
		(SELECT id FROM af.property WHERE code = 'config_20001.cfg'),
		(SELECT id FROM config_residual), false
	)
),
config_residual_config_20020_link AS (
	INSERT INTO af.property_config(
		order_number, creation_timestamp, creator_id,
		is_void, property_id, config_property_id, is_layout_variable
	) VALUES (
		1, 'now()', '1', false,
		(SELECT id FROM af.property WHERE code = 'config_20020.cfg'),
		(SELECT id FROM config_residual), false
	)
),
config_residual_config_20021_link AS (
	INSERT INTO af.property_config(
		order_number, creation_timestamp, creator_id,
		is_void, property_id, config_property_id, is_layout_variable
	) VALUES (
		1, 'now()', '1', false,
		(SELECT id FROM af.property WHERE code = 'config_20021.cfg'),
		(SELECT id FROM config_residual), false
	)
)
SELECT * FROM config_residual;


-- add residual:Autoregressive order 1 spatial structure (AR1row x AR1col) to config_20001, config_20020, config_20021
WITH config_residual AS (
	INSERT INTO af.property(
		type, data_type, code, "name", "label", "statement"
	) VALUES (
		'catalog_item', 'character varying', 'residual_opt2', 
		'Autoregressive order 1 spatial structure (AR1row x AR1col)', 
		'Autoregressive order 1 spatial structure (AR1row x AR1col)', 
		'ar1(row):ar1(col)'
	) RETURNING id
),
config_residual_property_config_link AS (
	INSERT INTO af.property_config(
		order_number, creation_timestamp, creator_id,
		is_void, property_id, config_property_id, is_layout_variable
	) VALUES (
		2, 'now()', '1', false,
		(SELECT id FROM af.property WHERE code='residual'), 
		(SELECT id FROM config_residual), false
	)
),
config_residual_config_20001_link AS (
	INSERT INTO af.property_config(
		order_number, creation_timestamp, creator_id,
		is_void, property_id, config_property_id, is_layout_variable
	) VALUES (
		2, 'now()', '1', false,
		(SELECT id FROM af.property WHERE code = 'config_20001.cfg'),
		(SELECT id FROM config_residual), false
	)
),
config_residual_config_20020_link AS (
	INSERT INTO af.property_config(
		order_number, creation_timestamp, creator_id,
		is_void, property_id, config_property_id, is_layout_variable
	) VALUES (
		2, 'now()', '1', false,
		(SELECT id FROM af.property WHERE code = 'config_20020.cfg'),
		(SELECT id FROM config_residual), false
	)
),
config_residual_config_20021_link AS (
	INSERT INTO af.property_config(
		order_number, creation_timestamp, creator_id,
		is_void, property_id, config_property_id, is_layout_variable
	) VALUES (
		2, 'now()', '1', false,
		(SELECT id FROM af.property WHERE code = 'config_20021.cfg'),
		(SELECT id FROM config_residual), false
	)
)
SELECT * FROM config_residual;


-- add residual:Autoregressive order 1 spatial structure for rows (AR1row x IDcol) to config_20001, config_20020, config_20021
WITH config_residual AS (
	INSERT INTO af.property(
		type, data_type, code, "name", "label", "statement"
	) VALUES (
		'catalog_item', 'character varying', 'residual_opt2', 
		'Autoregressive order 1 spatial structure for rows (AR1row x IDcol)', 
		'Autoregressive order 1 spatial structure for rows (AR1row x IDcol)', 
		'ar1(row):id(col)'
	) RETURNING id
),
config_residual_property_config_link AS (
	INSERT INTO af.property_config(
		order_number, creation_timestamp, creator_id,
		is_void, property_id, config_property_id, is_layout_variable
	) VALUES (
		3, 'now()', '1', false,
		(SELECT id FROM af.property WHERE code='residual'), 
		(SELECT id FROM config_residual), false
	)
),
config_residual_config_20001_link AS (
	INSERT INTO af.property_config(
		order_number, creation_timestamp, creator_id,
		is_void, property_id, config_property_id, is_layout_variable
	) VALUES (
		3, 'now()', '1', false,
		(SELECT id FROM af.property WHERE code = 'config_20001.cfg'),
		(SELECT id FROM config_residual), false
	)
),
config_residual_config_20020_link AS (
	INSERT INTO af.property_config(
		order_number, creation_timestamp, creator_id,
		is_void, property_id, config_property_id, is_layout_variable
	) VALUES (
		3, 'now()', '1', false,
		(SELECT id FROM af.property WHERE code = 'config_20020.cfg'),
		(SELECT id FROM config_residual), false
	)
),
config_residual_config_20021_link AS (
	INSERT INTO af.property_config(
		order_number, creation_timestamp, creator_id,
		is_void, property_id, config_property_id, is_layout_variable
	) VALUES (
		3, 'now()', '1', false,
		(SELECT id FROM af.property WHERE code = 'config_20021.cfg'),
		(SELECT id FROM config_residual), false
	)
)
SELECT * FROM config_residual;


-- add residual:Autoregressive order 1 spatial structure for cols (IDrow x AR1col) to config_20001, config_20020, config_20021
WITH config_residual AS (
	INSERT INTO af.property(
		type, data_type, code, "name", "label", "statement"
	) VALUES (
		'catalog_item', 'character varying', 'residual_opt2', 
		'Autoregressive order 1 spatial structure for cols (IDrow x AR1col)', 
		'Autoregressive order 1 spatial structure for cols (IDrow x AR1col)', 
		'id(row):ar1(col)'
	) RETURNING id
),
config_residual_property_config_link AS (
	INSERT INTO af.property_config(
		order_number, creation_timestamp, creator_id,
		is_void, property_id, config_property_id, is_layout_variable
	) VALUES (
		4, 'now()', '1', false,
		(SELECT id FROM af.property WHERE code='residual'), 
		(SELECT id FROM config_residual), false
	)
),
config_residual_config_20001_link AS (
	INSERT INTO af.property_config(
		order_number, creation_timestamp, creator_id,
		is_void, property_id, config_property_id, is_layout_variable
	) VALUES (
		4, 'now()', '1', false,
		(SELECT id FROM af.property WHERE code = 'config_20001.cfg'),
		(SELECT id FROM config_residual), false
	)
),
config_residual_config_20020_link AS (
	INSERT INTO af.property_config(
		order_number, creation_timestamp, creator_id,
		is_void, property_id, config_property_id, is_layout_variable
	) VALUES (
		4, 'now()', '1', false,
		(SELECT id FROM af.property WHERE code = 'config_20020.cfg'),
		(SELECT id FROM config_residual), false
	)
),
config_residual_config_20021_link AS (
	INSERT INTO af.property_config(
		order_number, creation_timestamp, creator_id,
		is_void, property_id, config_property_id, is_layout_variable
	) VALUES (
		4, 'now()', '1', false,
		(SELECT id FROM af.property WHERE code = 'config_20021.cfg'),
		(SELECT id FROM config_residual), false
	)
)
SELECT * FROM config_residual;


-- add prediction to config_20001
WITH config_prediction AS (
	INSERT INTO af.property(
		type, data_type, code, "name", "statement"
	) VALUES (
		'catalog_item', 'character varying', 'g', 'G', 'entry'
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
config_prediction_config_20001_link AS (
	INSERT INTO af.property_config(
		order_number, creation_timestamp, creator_id,
		is_void, property_id, config_property_id, is_layout_variable
	) VALUES (
		1, 'now()', '1', false,
		(SELECT id FROM af.property WHERE code = 'config_20001.cfg'),
		(SELECT id FROM config_prediction), false
	)

)
SELECT * FROM config_prediction;


-- add prediction to config_20020, config_20020 
WITH config_prediction AS (
	INSERT INTO af.property(
		type, data_type, code, "name", "statement"
	) VALUES (
		'catalog_item', 'character varying', 'g', 'G', 'ge'
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
config_prediction_config_20020_link AS (
	INSERT INTO af.property_config(
		order_number, creation_timestamp, creator_id,
		is_void, property_id, config_property_id, is_layout_variable
	) VALUES (
		1, 'now()', '1', false,
		(SELECT id FROM af.property WHERE code = 'config_20020.cfg'),
		(SELECT id FROM config_prediction), false
	)

),
config_prediction_config_20020_link AS (
	INSERT INTO af.property_config(
		order_number, creation_timestamp, creator_id,
		is_void, property_id, config_property_id, is_layout_variable
	) VALUES (
		1, 'now()', '1', false,
		(SELECT id FROM af.property WHERE code = 'config_20021.cfg'),
		(SELECT id FROM config_prediction), false
	)

)
SELECT * FROM config_prediction;
