--liquibase formatted sql

--changeset postgres:add_analysis_configuration_data context:template splitStatements:false rollbackSplitStatements:false
--comment: BA-11 Add analysis configuration data


-- OPTION 2: create catalog of fields and add metadata to them
 
-- Create Fields catalog
INSERT INTO af.property (id,code,"name","label",description,"type",data_type) VALUES (159,'analysis_module_fields','Analysis Module Fields','Analysis Module Fields','Analysis Module Fields','catalog_root','character varying');
INSERT INTO af.property_config (order_number,creation_timestamp,creator_id,is_void,property_id,config_property_id,is_layout_variable) VALUES (1,'now()','1',false,159,159,false);

INSERT INTO af.property (id, code, type,data_type) VALUES    -- Data type/Stat_factor
	(160,'loc','catalog_item','!A'),
	(161,'expt','catalog_item','!A'),
	(162,'entry','catalog_item','!A'),
	(163,'plot','catalog_item','!A'),
	(164,'col','catalog_item','!I'),
	(165,'row','catalog_item','!I'),
	(166,'rep','catalog_item','!A'),
	(167,'block','catalog_item','!A');

INSERT INTO af.property_config (order_number,creation_timestamp,creator_id,is_void,property_id,config_property_id,is_layout_variable) VALUES 
	(1,'now()','1',false,159,160,false),
	(2,'now()','1',false,159,161,false),
	(3,'now()','1',false,159,162,false),
	(4,'now()','1',false,159,163,false),
	(5,'now()','1',false,159,164,false),
	(6,'now()','1',false,159,165,false),
	(7,'now()','1',false,159,166,false),
	(8,'now()','1',false,159,167,false);

	-- meta in catalog
INSERT INTO af.property_meta(code,value,property_id)values --Fields metadata (Definition/Condition)
	('definition','loc_id',160),
	('condition','!SORTALL !PRUNEALL',160),
	('definition','expt_id',161),
	('condition','!LL 32',161),
	('definition','entry_id',162),
	('definition','plot_id',163),
	('definition','pa_x',164),
	('definition','pa_y',165),
	('definition','rep_factor',166),
	('definition','blk',167);

-- catalogos de compoenntes  de una configuracion
INSERT INTO af.property (code,"name","label",description,"type",data_type,id) VALUES ('analysis_config','Analysis Configuration','Analysis Configuration','Analysis Configuration','catalog_root','character varying',134);
--INSERT INTO af.property (code,"name","label",description,"type",data_type,id) VALUES ('analysis_info','Analysis Information','Analysis Information','Analysis Information','analysis_config_element','character varying',135);
--INSERT INTO af.property (code,"name","label",description,"type",data_type,id) VALUES ('experiment_info','Experiment Information','Experiment Information','Experiment Information','analysis_config_element','character varying',136);
INSERT INTO af.property (code,"name","label",description,"type",data_type,id) VALUES ('asrmel_options','ASRMEL Options','ASRMEL Options','ASRMEL Options','catalog_root','character varying',137);
INSERT INTO af.property (code,"name","label",description,"type",data_type,id) VALUES ('tabulate','Tabulate','Tabulate','Tabulate','catalog_root','character varying',138);
INSERT INTO af.property (code,"name","label",description,"type",data_type,id) VALUES ('formula','Formula','Formula','Formula','catalog_root','character varying',139);
INSERT INTO af.property (code,"name","label",description,"type",data_type,id) VALUES ('residual','Residual','Residual','Residual','catalog_root','character varying',140);

INSERT INTO af.property_config (order_number,creation_timestamp,creator_id,is_void,property_id,config_property_id,is_layout_variable) VALUES (1,'now()','1',false,134,142,false);
INSERT INTO af.property_config (order_number,creation_timestamp,creator_id,is_void,property_id,config_property_id,is_layout_variable) VALUES (2,'now()','1',false,134,143,false);
INSERT INTO af.property_config (order_number,creation_timestamp,creator_id,is_void,property_id,config_property_id,is_layout_variable) VALUES (3,'now()','1',false,134,144,false);
INSERT INTO af.property_config (order_number,creation_timestamp,creator_id,is_void,property_id,config_property_id,is_layout_variable) VALUES (4,'now()','1',false,134,145,false);
INSERT INTO af.property_config (order_number,creation_timestamp,creator_id,is_void,property_id,config_property_id,is_layout_variable) VALUES (7,'now()','1',false,134,134,false);
--predict is id=5
INSERT INTO af.property_config (order_number,creation_timestamp,creator_id,is_void,property_id,config_property_id,is_layout_variable) VALUES (7,'now()','1',false,137,137,false);
INSERT INTO af.property_config (order_number,creation_timestamp,creator_id,is_void,property_id,config_property_id,is_layout_variable) VALUES (8,'now()','1',false,138,138,false);
INSERT INTO af.property_config (order_number,creation_timestamp,creator_id,is_void,property_id,config_property_id,is_layout_variable) VALUES (9,'now()','1',false,139,139,false);
INSERT INTO af.property_config (order_number,creation_timestamp,creator_id,is_void,property_id,config_property_id,is_layout_variable) VALUES (10,'now()','1',false,140,140,false);

/* configs*/
INSERT INTO af.property (code,"name","label",description,"type",data_type,id) VALUES ('config_00001.cfg','RCBD univariate','RCBD univariate','RCBD single loc, single year and univariate trial with options for spatial adjustment','catalog_item','character varying',142);
INSERT INTO af.property (code,"name","label",description,"type",data_type,id) VALUES ('config_00002.cfg','RCBD multi-location univariate','RCBD multi-location univariate','RCBD multi-location and univariate trial with options for spatial adjustment','catalog_item','character varying',143);
INSERT INTO af.property (code,"name","label",description,"type",data_type,id) VALUES ('config_00003.cfg','Alpha-Lattice univariate','Alpha-Lattice univariate','Alpha-Lattice single loc, single year and univariate trial with options for spatial adjustment','catalog_item','character varying',144);
INSERT INTO af.property (code,"name","label",description,"type",data_type,id) VALUES ('config_00004.cfg','Alpha-Lattice multi-location univariate','Alpha-Lattice multi-location univariate','Alpha-Lattice multi-location and univariate trial with options for spatial adjustment','catalog_item','character varying',145);


-- fields to configs
INSERT INTO af.property_config (order_number,creation_timestamp,creator_id,is_void,property_id,config_property_id,is_layout_variable) VALUES 
	(9,'now()','1',false,142,160,false),
	(10,'now()','1',false,142,161,false),
	(11,'now()','1',false,142,162,false),
	(12,'now()','1',false,142,163,false),
	(13,'now()','1',false,142,164,false),
	(14,'now()','1',false,142,165,false),
	(15,'now()','1',false,142,166,false),
	(10,'now()','1',false,143,160,false),
	(11,'now()','1',false,143,161,false),
	(12,'now()','1',false,143,162,false),
	(13,'now()','1',false,143,163,false),
	(14,'now()','1',false,143,164,false),
	(15,'now()','1',false,143,165,false),
	(16,'now()','1',false,143,166,false),
	(9,'now()','1',false,144,160,false),
	(10,'now()','1',false,144,161,false),
	(11,'now()','1',false,144,162,false),
	(12,'now()','1',false,144,163,false),
	(13,'now()','1',false,144,164,false),
	(14,'now()','1',false,144,165,false),
	(15,'now()','1',false,144,166,false),
	(16,'now()','1',false,144,167,false),
	(10,'now()','1',false,145,160,false),
	(11,'now()','1',false,145,161,false),
	(12,'now()','1',false,145,162,false),
	(13,'now()','1',false,145,163,false),
	(14,'now()','1',false,145,164,false),
	(15,'now()','1',false,145,165,false),
	(16,'now()','1',false,145,166,false),
	(17,'now()','1',false,145,167,false);


INSERT INTO af.property_meta(code,value,property_id)values
	('config_version','1.0.1', 142),
	('date','21-Sep-2020', 142),
	('author','Pedro Barbosa', 142),
	('email','p.medeiros@cgiar.org', 142),
	('engine','ASREML', 142),
    ('design','RCBD', 142),
	('trait_level','plot',142),
    ('analysis_objective', 'prediction', 142),
    ('exp_analysis_pattern', 'single', 142),
    ('loc_analysis_pattern','single', 142),
    ('year_analysis_pattern', 'single', 142),
    ('trait_pattern','univariate', 142),

	('config_version','1.0.1', 143),
	('date','03-Sep-2020', 143),
	('author','Pedro Barbosa', 143),
	('email','p.medeiros@cgiar.org', 143),
	('engine','ASREML', 143),
	('design','RCBD', 143),
	('trait_level','plot',143),
    ('analysis_objective', 'prediction', 143),
    ('exp_analysis_pattern', 'single', 143),
    ('loc_analysis_pattern','multi', 143),
    ('year_analysis_pattern', 'single', 143),
    ('trait_pattern','univariate', 143),

	('config_version','1.0.1', 144),
	('date','21-Sep-2020', 144),
	('author','Pedro Barbosa', 144),
	('email','p.medeiros@cgiar.org', 144),
	('engine','ASREML', 144),
	('design','Alpha-Lattice', 144),
	('trait_level','plot',144),
    ('analysis_objective', 'prediction', 144),
    ('exp_analysis_pattern', 'single', 144),
    ('loc_analysis_pattern','single', 144),
    ('year_analysis_pattern', 'single', 144),
    ('trait_pattern','univariate', 144),

	('config_version','1.0.1', 145),
	('date','03-Sep-2020', 145),
	('author','Pedro Barbosa', 145),
	('email','p.medeiros@cgiar.org', 145),
	('engine','ASREML', 145),
	('design','Alpha-Lattice', 145),
	('trait_level','plot',145),
    ('analysis_objective', 'prediction', 145),
    ('exp_analysis_pattern', 'single', 145),
    ('loc_analysis_pattern','multi', 145),
    ('year_analysis_pattern', 'single', 145),
    ('trait_pattern','univariate', 145);


/*asrmel options*/
INSERT INTO af.property (id,type,data_type,code,"statement") VALUES (146,'catalog_item','character varying','asrmel_opt1','!CSV !SKIP 1 !AKAIKE !NODISPLAY 1 !MVINCLUDE !MAXIT 250 !EXTRA 10 !TXTFORM 1 !FCON !SUM !OUTLIER');
	INSERT INTO af.property_config (order_number,creation_timestamp,creator_id,is_void,property_id,config_property_id,is_layout_variable) VALUES (1,'now()','1',false,137,146,false);

/*tabulate*/
INSERT INTO af.property (id,type,data_type,code,"name","label","statement") VALUES (147,'catalog_item','character varying','tabulate_opt1','trait by entry','trait by entry','{trait_name} ~ entry');
	INSERT INTO af.property_config (order_number,creation_timestamp,creator_id,is_void,property_id,config_property_id,is_layout_variable) VALUES (1,'now()','1',false,138,147,false);

/*formula*/
INSERT INTO af.property (id,type,data_type,code,"name","label","statement") VALUES (148,'catalog_item','character varying','formula_opt1','RCBD SESL Univariate entry as random','RCBD SESL Univariate entry as random','{trait_name} ~ mu rep !r entry !f mv');
INSERT INTO af.property (id,type,data_type,code,"name","label","statement") VALUES (149,'catalog_item','character varying','formula_opt2','RCBD SEML Univariate','RCBD SEML Univariate','{trait_name} ~ mu rep loc !r entry entry.loc loc.rep !f mv');
INSERT INTO af.property (id,type,data_type,code,"name","label","statement") VALUES (150,'catalog_item','character varying','formula_opt3','Alpha-Lattice single location, univariate, entry as random factor','Alpha-Lattice single location, univariate, entry as random factor','{trait_name} mu rep !r entry rep.block !f mv');
INSERT INTO af.property (id,type,data_type,code,"name","label","statement") VALUES (151,'catalog_item','character varying','formula_opt4','Alpha-Lattice MET Univariate','Alpha-Lattice MET Univariate','{trait_name} ~ mu loc loc.rep !r loc.rep.block entry entry.loc !f mv');
	INSERT INTO af.property_config (order_number,creation_timestamp,creator_id,is_void,property_id,config_property_id,is_layout_variable) VALUES (1,'now()','1',false,139,148,false);
	INSERT INTO af.property_config (order_number,creation_timestamp,creator_id,is_void,property_id,config_property_id,is_layout_variable) VALUES (1,'now()','1',false,139,149,false);
	INSERT INTO af.property_config (order_number,creation_timestamp,creator_id,is_void,property_id,config_property_id,is_layout_variable) VALUES (1,'now()','1',false,139,150,false);
	INSERT INTO af.property_config (order_number,creation_timestamp,creator_id,is_void,property_id,config_property_id,is_layout_variable) VALUES (1,'now()','1',false,139,151,false);

/*residual*/
INSERT INTO af.property (id,type,data_type,code,"name","label","description","statement") VALUES (152,'catalog_item','character varying','residual_opt1','(AR1row x AR1col)','(AR1row x AR1col)','Autoregressive order 1 spatial structure (AR1row x AR1col)','ar1(row).ar1(col)');
INSERT INTO af.property (id,type,data_type,code,"name","label","description","statement") VALUES (153,'catalog_item','character varying','residual_opt2','(IDrow x AR1col)','(IDrow x AR1col)','Autoregressive order 1 spatial structure for columns (IDrow x AR1col)','idv(row).ar1(col)');
INSERT INTO af.property (id,type,data_type,code,"name","label","description","statement") VALUES (154,'catalog_item','character varying','residual_opt3','(AR1row x IDcol)','(AR1row x IDcol)','Autoregressive order 1 spatial structure for rows (AR1row x IDcol)','ar1(row).idv(col)');
INSERT INTO af.property (id,type,data_type,code,"name","label","description","statement") VALUES (155,'catalog_item','character varying','residual_opt4','No spatial adjustment','No spatial adjustment', null,null);
INSERT INTO af.property (id,type,data_type,code,"name","label","description","statement") VALUES (156,'catalog_item','character varying','residual_opt5','(AR1row x AR1col) by location','(AR1row x AR1col) by location','Autoregressive order 1 spatial structure (AR1row x AR1col), by location','sat(loc).idv(row).ar1(col)');
INSERT INTO af.property (id,type,data_type,code,"name","label","description","statement") VALUES (157,'catalog_item','character varying','residual_opt6','(IDrow x AR1col) by location','(IDrow x AR1col) by location','Autoregressive order 1 spatial structure for columns (IDrow x AR1col), by location','sat(loc).idv(row).ar1(col)');
INSERT INTO af.property (id,type,data_type,code,"name","label","description","statement") VALUES (158,'catalog_item','character varying','residual_opt7','(AR1row x IDcol) by location','(AR1row x IDcol) by location','Autoregressive order 1 spatial structure for rows (AR1row x IDcol), by location','sat(loc).ar1(row).idv(col)');
	INSERT INTO af.property_config (order_number,creation_timestamp,creator_id,is_void,property_id,config_property_id,is_layout_variable) VALUES (1,'now()','1',false,140,152,false);
	INSERT INTO af.property_config (order_number,creation_timestamp,creator_id,is_void,property_id,config_property_id,is_layout_variable) VALUES (1,'now()','1',false,140,153,false);
	INSERT INTO af.property_config (order_number,creation_timestamp,creator_id,is_void,property_id,config_property_id,is_layout_variable) VALUES (1,'now()','1',false,140,154,false);
	INSERT INTO af.property_config (order_number,creation_timestamp,creator_id,is_void,property_id,config_property_id,is_layout_variable) VALUES (1,'now()','1',false,140,155,false);
	INSERT INTO af.property_config (order_number,creation_timestamp,creator_id,is_void,property_id,config_property_id,is_layout_variable) VALUES (1,'now()','1',false,140,156,false);
	INSERT INTO af.property_config (order_number,creation_timestamp,creator_id,is_void,property_id,config_property_id,is_layout_variable) VALUES (1,'now()','1',false,140,157,false);
	INSERT INTO af.property_config (order_number,creation_timestamp,creator_id,is_void,property_id,config_property_id,is_layout_variable) VALUES (1,'now()','1',false,140,158,false);

/*predict / error: ya existía*/
update af.property set "statement" = 'entry !PRESENT entry !SED !TDIFF' where id = 19;
update af.property set "statement" = 'loc.entry !PRESENT loc entry !SED !TDIFF' where id = 20;

/*config 1*/
	INSERT INTO af.property_config (order_number,creation_timestamp,creator_id,is_void,property_id,config_property_id,is_layout_variable) VALUES (1,'now()','1',false,142,146,false);
	INSERT INTO af.property_config (order_number,creation_timestamp,creator_id,is_void,property_id,config_property_id,is_layout_variable) VALUES (2,'now()','1',false,142,147,false);
	INSERT INTO af.property_config (order_number,creation_timestamp,creator_id,is_void,property_id,config_property_id,is_layout_variable) VALUES (3,'now()','1',false,142,148,false);
	INSERT INTO af.property_config (order_number,creation_timestamp,creator_id,is_void,property_id,config_property_id,is_layout_variable) VALUES (4,'now()','1',false,142,152,false);
	INSERT INTO af.property_config (order_number,creation_timestamp,creator_id,is_void,property_id,config_property_id,is_layout_variable) VALUES (5,'now()','1',false,142,153,false);
	INSERT INTO af.property_config (order_number,creation_timestamp,creator_id,is_void,property_id,config_property_id,is_layout_variable) VALUES (6,'now()','1',false,142,154,false);
	INSERT INTO af.property_config (order_number,creation_timestamp,creator_id,is_void,property_id,config_property_id,is_layout_variable) VALUES (7,'now()','1',false,142,155,false);
	INSERT INTO af.property_config (order_number,creation_timestamp,creator_id,is_void,property_id,config_property_id,is_layout_variable) VALUES (8,'now()','1',false,142,19,false);

/*config 2*/
	INSERT INTO af.property_config (order_number,creation_timestamp,creator_id,is_void,property_id,config_property_id,is_layout_variable) VALUES (1,'now()','1',false,143,146,false);
	INSERT INTO af.property_config (order_number,creation_timestamp,creator_id,is_void,property_id,config_property_id,is_layout_variable) VALUES (2,'now()','1',false,143,147,false);
	INSERT INTO af.property_config (order_number,creation_timestamp,creator_id,is_void,property_id,config_property_id,is_layout_variable) VALUES (3,'now()','1',false,143,149,false);
	INSERT INTO af.property_config (order_number,creation_timestamp,creator_id,is_void,property_id,config_property_id,is_layout_variable) VALUES (4,'now()','1',false,143,156,false);
	INSERT INTO af.property_config (order_number,creation_timestamp,creator_id,is_void,property_id,config_property_id,is_layout_variable) VALUES (5,'now()','1',false,143,157,false);
	INSERT INTO af.property_config (order_number,creation_timestamp,creator_id,is_void,property_id,config_property_id,is_layout_variable) VALUES (6,'now()','1',false,143,158,false);
	INSERT INTO af.property_config (order_number,creation_timestamp,creator_id,is_void,property_id,config_property_id,is_layout_variable) VALUES (7,'now()','1',false,143,155,false);
	INSERT INTO af.property_config (order_number,creation_timestamp,creator_id,is_void,property_id,config_property_id,is_layout_variable) VALUES (8,'now()','1',false,143,19,false);
	INSERT INTO af.property_config (order_number,creation_timestamp,creator_id,is_void,property_id,config_property_id,is_layout_variable) VALUES (9,'now()','1',false,143,20,false);

/*config 3*/
	INSERT INTO af.property_config (order_number,creation_timestamp,creator_id,is_void,property_id,config_property_id,is_layout_variable) VALUES (1,'now()','1',false,144,146,false);
	INSERT INTO af.property_config (order_number,creation_timestamp,creator_id,is_void,property_id,config_property_id,is_layout_variable) VALUES (2,'now()','1',false,144,147,false);
	INSERT INTO af.property_config (order_number,creation_timestamp,creator_id,is_void,property_id,config_property_id,is_layout_variable) VALUES (3,'now()','1',false,144,150,false);
	INSERT INTO af.property_config (order_number,creation_timestamp,creator_id,is_void,property_id,config_property_id,is_layout_variable) VALUES (4,'now()','1',false,144,152,false);
	INSERT INTO af.property_config (order_number,creation_timestamp,creator_id,is_void,property_id,config_property_id,is_layout_variable) VALUES (5,'now()','1',false,144,153,false);
	INSERT INTO af.property_config (order_number,creation_timestamp,creator_id,is_void,property_id,config_property_id,is_layout_variable) VALUES (6,'now()','1',false,144,154,false);
	INSERT INTO af.property_config (order_number,creation_timestamp,creator_id,is_void,property_id,config_property_id,is_layout_variable) VALUES (7,'now()','1',false,144,155,false);
	INSERT INTO af.property_config (order_number,creation_timestamp,creator_id,is_void,property_id,config_property_id,is_layout_variable) VALUES (8,'now()','1',false,144,19,false);
	
/*config 4*/
	INSERT INTO af.property_config (order_number,creation_timestamp,creator_id,is_void,property_id,config_property_id,is_layout_variable) VALUES (1,'now()','1',false,145,146,false);
	INSERT INTO af.property_config (order_number,creation_timestamp,creator_id,is_void,property_id,config_property_id,is_layout_variable) VALUES (2,'now()','1',false,145,147,false);
	INSERT INTO af.property_config (order_number,creation_timestamp,creator_id,is_void,property_id,config_property_id,is_layout_variable) VALUES (3,'now()','1',false,145,151,false);
	INSERT INTO af.property_config (order_number,creation_timestamp,creator_id,is_void,property_id,config_property_id,is_layout_variable) VALUES (4,'now()','1',false,145,156,false);
	INSERT INTO af.property_config (order_number,creation_timestamp,creator_id,is_void,property_id,config_property_id,is_layout_variable) VALUES (5,'now()','1',false,145,157,false);
	INSERT INTO af.property_config (order_number,creation_timestamp,creator_id,is_void,property_id,config_property_id,is_layout_variable) VALUES (6,'now()','1',false,145,158,false);
	INSERT INTO af.property_config (order_number,creation_timestamp,creator_id,is_void,property_id,config_property_id,is_layout_variable) VALUES (7,'now()','1',false,145,155,false);
	INSERT INTO af.property_config (order_number,creation_timestamp,creator_id,is_void,property_id,config_property_id,is_layout_variable) VALUES (8,'now()','1',false,145,19,false);
	INSERT INTO af.property_config (order_number,creation_timestamp,creator_id,is_void,property_id,config_property_id,is_layout_variable) VALUES (9,'now()','1',false,145,20,false);