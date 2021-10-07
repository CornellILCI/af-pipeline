--liquibase formatted sql

--changeset postgres:add_2_new_models_for_irri_config5_config6 context:template splitStatements:false rollbackSplitStatements:false
--comment: DB-692 Add 2 new models for IRRI, Config5 and config6


/* new property config_00005.cfg/config_00006.cfg*/
INSERT INTO af.property
(code, "name", "label", description, "type", data_type, creator_id, is_void, tenant_id, id, "statement")
VALUES
('config_00005.cfg', 'Row-Column univariate', 'Row-Column univariate', 'Row-Column single loc, single year and univariate trial with options for spatial adjustment', 'catalog_item', 'character varying', '1', false, 1, 194, NULL),
('config_00006.cfg', 'Row-Column multi-location univariate', 'Row-Column multi-location univariate', 'Row-Column multi-location and univariate trial with options for spatial adjustment', 'catalog_item', 'character varying', '1', false, 1, 195, NULL)
;

INSERT INTO af.property (id, code, type,data_type) VALUES    -- Data type/Stat_factor
	(196,'rowblock','catalog_item','!A'),
	(197,'colblock','catalog_item','!A');

	-- meta in catalog
INSERT INTO af.property_meta(code,value,property_id)values --Fields metadata (Definition/Condition)
	('definition','rowblk',196),
	('condition','',196),
    ('definition','colblk',197),
	('condition','',197);

INSERT INTO af.property_config
(is_required, order_number, creator_id, is_void, tenant_id, id, property_id, config_property_id, property_ui_id, is_layout_variable)
VALUES
(false, 10, '1', false, 1, 312, 4, 194, NULL, false),
(false, 11, '1', false, 1, 313, 4, 195, NULL, false),
(false, 12,'1',false,1, 314, 159,196, NULL, false),
(false, 13,'1',false,1, 315, 159,197, NULL, false)
;

select setval('af.property_config_id_seq',max(id)) from af.property_config;

/*config_00005 metadata*/
insert into af.property_meta(property_id,code,value,tenant_id) values
(194,'Version','1.0.0',1),
(194,'date','21-Sep-2020',1),
(194,'author','Pedro Barbosa | Alaine Gulles',1),
(194,'email','p.medeiros@cgiar.org | a.gulles@irri.org',1),
(194,'organization_code','null',1),
(194,'engine','ASREML',1),

(194,'breding_program_id','null',1),
(194,'pipeline_id','null',1),
(194,'stage_id','null',1),
(194,'note',' ',1),
(194,'design','Row-Column',1),

(194,'trait_level','plot',1),
(194,'analysis_objective','prediction',1),
(194,'exp_analysis_pattern','single',1),
(194,'loc_analysis_pattern','single',1),
(194,'year_analysis_pattern','single',1),
(194,'trait_pattern','univariate',1);

/*config_00006 metadata*/
insert into af.property_meta(property_id,code,value,tenant_id) values
(195,'Version','1.0.0',1),
(195,'date','01-Feb-2021',1),
(195,'author','Pedro Barbosa, Alaine Gulles',1),
(195,'email','p.medeiros@cgiar.org, a.gulles@irri.org',1),
(195,'organization_code','null',1),
(195,'engine','ASREML',1),

(195,'breding_program_id','null',1),
(195,'pipeline_id','null',1),
(195,'stage_id','null',1),
(195,'note',' ',1),
(195,'design','Row-Column',1),

(195,'trait_level','plot',1),
(195,'analysis_objective','prediction',1),
(195,'exp_analysis_pattern','single',1),
(195,'loc_analysis_pattern','multi',1),
(195,'year_analysis_pattern','single',1),
(195,'trait_pattern','univariate',1);




/*config 5*/    
INSERT INTO af.property_config (order_number,creator_id,is_void,property_id,config_property_id,is_layout_variable) VALUES (1,'1',false,194,146,false);
INSERT INTO af.property_config (order_number,creator_id,is_void,property_id,config_property_id,is_layout_variable) VALUES (2,'1',false,194,147,false);
INSERT INTO af.property_config (order_number,creator_id,is_void,property_id,config_property_id,is_layout_variable) VALUES (3,'1',false,194,149,false);
INSERT INTO af.property_config (order_number,creator_id,is_void,property_id,config_property_id,is_layout_variable) VALUES (4,'1',false,194,155,false);
INSERT INTO af.property_config (order_number,creator_id,is_void,property_id,config_property_id,is_layout_variable) VALUES (5,'1',false,194,156,false);
INSERT INTO af.property_config (order_number,creator_id,is_void,property_id,config_property_id,is_layout_variable) VALUES (6,'1',false,194,157,false);
INSERT INTO af.property_config (order_number,creator_id,is_void,property_id,config_property_id,is_layout_variable) VALUES (7,'1',false,194,158,false);
INSERT INTO af.property_config (order_number,creator_id,is_void,property_id,config_property_id,is_layout_variable) VALUES (8,'1',false,194,19,false);
INSERT INTO af.property_config (order_number,creator_id,is_void,property_id,config_property_id,is_layout_variable) VALUES (9,'1',false,194,20,false);
INSERT INTO af.property_config (order_number,creator_id,is_void,property_id,config_property_id,is_layout_variable) VALUES (10,'1',false,194,160,false);
INSERT INTO af.property_config (order_number,creator_id,is_void,property_id,config_property_id,is_layout_variable) VALUES (11,'1',false,194,161,false);
INSERT INTO af.property_config (order_number,creator_id,is_void,property_id,config_property_id,is_layout_variable) VALUES (12,'1',false,194,162,false);
INSERT INTO af.property_config (order_number,creator_id,is_void,property_id,config_property_id,is_layout_variable) VALUES (13,'1',false,194,163,false);
INSERT INTO af.property_config (order_number,creator_id,is_void,property_id,config_property_id,is_layout_variable) VALUES (14,'1',false,194,164,false);
INSERT INTO af.property_config (order_number,creator_id,is_void,property_id,config_property_id,is_layout_variable) VALUES (15,'1',false,194,165,false);
INSERT INTO af.property_config (order_number,creator_id,is_void,property_id,config_property_id,is_layout_variable) VALUES (16,'1',false,194,166,false);


/*config 6*/    
INSERT INTO af.property_config (order_number,creator_id,is_void,property_id,config_property_id,is_layout_variable) VALUES (1,'1',false,195,146,false);
INSERT INTO af.property_config (order_number,creator_id,is_void,property_id,config_property_id,is_layout_variable) VALUES (2,'1',false,195,147,false);
INSERT INTO af.property_config (order_number,creator_id,is_void,property_id,config_property_id,is_layout_variable) VALUES (3,'1',false,195,151,false);
INSERT INTO af.property_config (order_number,creator_id,is_void,property_id,config_property_id,is_layout_variable) VALUES (4,'1',false,195,156,false);
INSERT INTO af.property_config (order_number,creator_id,is_void,property_id,config_property_id,is_layout_variable) VALUES (5,'1',false,195,157,false);
INSERT INTO af.property_config (order_number,creator_id,is_void,property_id,config_property_id,is_layout_variable) VALUES (6,'1',false,195,158,false);
INSERT INTO af.property_config (order_number,creator_id,is_void,property_id,config_property_id,is_layout_variable) VALUES (7,'1',false,195,192,false);
INSERT INTO af.property_config (order_number,creator_id,is_void,property_id,config_property_id,is_layout_variable) VALUES (8,'1',false,195,19,false);
INSERT INTO af.property_config (order_number,creator_id,is_void,property_id,config_property_id,is_layout_variable) VALUES (9,'1',false,195,20,false);
INSERT INTO af.property_config (order_number,creator_id,is_void,property_id,config_property_id,is_layout_variable) VALUES (10,'1',false,195,160,false);
INSERT INTO af.property_config (order_number,creator_id,is_void,property_id,config_property_id,is_layout_variable) VALUES (11,'1',false,195,161,false);
INSERT INTO af.property_config (order_number,creator_id,is_void,property_id,config_property_id,is_layout_variable) VALUES (12,'1',false,195,162,false);
INSERT INTO af.property_config (order_number,creator_id,is_void,property_id,config_property_id,is_layout_variable) VALUES (13,'1',false,195,163,false);
INSERT INTO af.property_config (order_number,creator_id,is_void,property_id,config_property_id,is_layout_variable) VALUES (14,'1',false,195,164,false);
INSERT INTO af.property_config (order_number,creator_id,is_void,property_id,config_property_id,is_layout_variable) VALUES (15,'1',false,195,165,false);
INSERT INTO af.property_config (order_number,creator_id,is_void,property_id,config_property_id,is_layout_variable) VALUES (16,'1',false,195,166,false);
INSERT INTO af.property_config (order_number,creator_id,is_void,property_id,config_property_id,is_layout_variable) VALUES (17,'1',false,195,196,false);
INSERT INTO af.property_config (order_number,creator_id,is_void,property_id,config_property_id,is_layout_variable) VALUES (18,'1',false,195,197,false);

select setval('af.property_config_id_seq',max(id)) from af.property_config;
select setval('af.property_id_seq',max(id)) from af.property;


--Revert Changes
--rollback DELETE FROM af.property_config WHERE property_id = 195;
--rollback DELETE FROM af.property_config WHERE property_id = 194;
--rollback DELETE FROM af.property_meta WHERE property_id = 194;
--rollback DELETE FROM af.property_meta WHERE property_id = 195;
--rollback DELETE FROM af.property_config WHERE id IN (312, 313, 314, 315);
--rollback DELETE FROM af.property_meta WHERE property_id IN (196, 197);
--rollback DELETE FROM af.property WHERE id IN (196, 197, 194, 195);
--rollback select setval('af.property_config_id_seq',max(id)) from af.property_config;
--rollback select setval('af.property_id_seq',max(id)) from af.property;