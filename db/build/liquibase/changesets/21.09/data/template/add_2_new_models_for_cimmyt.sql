--liquibase formatted sql

--changeset postgres:add_models_for_cimmyt_config7_config8 context:template splitStatements:false rollbackSplitStatements:false
--comment: DB-692 Add 2 new models for CIMMYT


/* new property config_00007.cfg/config_00008.cfg*/
INSERT INTO af.property
(code, "name", "label", description, "type", data_type, creator_id, is_void, tenant_id, id, "statement")
VALUES
('config_00007.cfg', 'RCBD MET univariate - heterogeneous genetic variances within environments', 'RCBD MET univariate - heterogeneous genetic variances within environments', 'RCBD multi-location with heterogeneous genetic variances within environments, univariate trial with options for spatial adjustment', 'catalog_item', 'character varying', '1', false, 1, 198, NULL),
('config_00008.cfg', 'Alpha-Lattice MET univariate - heterogeneous genetic variances within environments', 'Alpha-Lattice MET univariate - heterogeneous genetic variances within environments', 'Alpha-Lattice multi-location, with heterogeneous genetic variances within environments and univariate trial with options for spatial adjustment', 'catalog_item', 'character varying', '1', false, 1, 199, NULL)
;

INSERT INTO af.property_config
(is_required, order_number, creator_id, is_void, tenant_id, id, property_id, config_property_id, property_ui_id, is_layout_variable)
VALUES
(false, 12, '1', false, 1, 352, 4, 198, NULL, false),
(false, 13, '1', false, 1, 353, 4, 199, NULL, false)
;

select setval('af.property_config_id_seq',max(id)) from af.property_config;

/*config_00007 metadata*/
insert into af.property_meta(property_id,code,value,tenant_id) values
(198,'Version','1.0.1',1),
(198,'date','18-Jul-2021',1),
(198,'author','Pedro Barbosa',1),
(198,'email','p.medeiros@cgiar.org',1),
(198,'organization_code','null',1),
(198,'engine','ASREML',1),

(198,'breding_program_id','null',1),
(198,'pipeline_id','null',1),
(198,'stage_id','null',1),
(198,'design','RCBD',1),
(198,'design','Augmented-RCB',1),

(198,'trait_level','plot',1),
(198,'analysis_objective','prediction',1),
(198,'exp_analysis_pattern','single',1),
(198,'loc_analysis_pattern','multi',1),
(198,'year_analysis_pattern','single',1),
(198,'trait_pattern','univariate',1);

/*config_00008 metadata*/
insert into af.property_meta(property_id,code,value,tenant_id) values
(199,'Version','1.0.1',1),
(199,'date','20-Jul-2021',1),
(199,'author','Pedro Barbosa',1),
(199,'email','p.medeiros@cgiar.org',1),
(199,'organization_code','null',1),
(199,'engine','ASREML',1),

(199,'breding_program_id','null',1),
(199,'pipeline_id','null',1),
(199,'stage_id','null',1),
(199,'design','Alpha-Lattice',1),

(199,'trait_level','plot',1),
(199,'analysis_objective','prediction',1),
(199,'exp_analysis_pattern','single',1),
(199,'loc_analysis_pattern','multi',1),
(199,'year_analysis_pattern','single',1),
(199,'trait_pattern','univariate',1);




/*config 5*/    
INSERT INTO af.property_config (order_number,creator_id,is_void,property_id,config_property_id,is_layout_variable) VALUES (1,'1',false,198,146,false);
INSERT INTO af.property_config (order_number,creator_id,is_void,property_id,config_property_id,is_layout_variable) VALUES (2,'1',false,198,147,false);
INSERT INTO af.property_config (order_number,creator_id,is_void,property_id,config_property_id,is_layout_variable) VALUES (3,'1',false,198,149,false);
INSERT INTO af.property_config (order_number,creator_id,is_void,property_id,config_property_id,is_layout_variable) VALUES (5,'1',false,198,156,false);
INSERT INTO af.property_config (order_number,creator_id,is_void,property_id,config_property_id,is_layout_variable) VALUES (6,'1',false,198,157,false);
INSERT INTO af.property_config (order_number,creator_id,is_void,property_id,config_property_id,is_layout_variable) VALUES (7,'1',false,198,158,false);
INSERT INTO af.property_config (order_number,creator_id,is_void,property_id,config_property_id,is_layout_variable) VALUES (7,'1',false,198,192,false);
INSERT INTO af.property_config (order_number,creator_id,is_void,property_id,config_property_id,is_layout_variable) VALUES (8,'1',false,198,19,false);
INSERT INTO af.property_config (order_number,creator_id,is_void,property_id,config_property_id,is_layout_variable) VALUES (9,'1',false,198,20,false);
INSERT INTO af.property_config (order_number,creator_id,is_void,property_id,config_property_id,is_layout_variable) VALUES (10,'1',false,198,160,false);
INSERT INTO af.property_config (order_number,creator_id,is_void,property_id,config_property_id,is_layout_variable) VALUES (11,'1',false,198,161,false);
INSERT INTO af.property_config (order_number,creator_id,is_void,property_id,config_property_id,is_layout_variable) VALUES (12,'1',false,198,162,false);
INSERT INTO af.property_config (order_number,creator_id,is_void,property_id,config_property_id,is_layout_variable) VALUES (13,'1',false,198,163,false);
INSERT INTO af.property_config (order_number,creator_id,is_void,property_id,config_property_id,is_layout_variable) VALUES (14,'1',false,198,164,false);
INSERT INTO af.property_config (order_number,creator_id,is_void,property_id,config_property_id,is_layout_variable) VALUES (15,'1',false,198,165,false);
INSERT INTO af.property_config (order_number,creator_id,is_void,property_id,config_property_id,is_layout_variable) VALUES (16,'1',false,198,166,false);


/*config 6*/    
INSERT INTO af.property_config (order_number,creator_id,is_void,property_id,config_property_id,is_layout_variable) VALUES (1,'1',false,199,146,false);
INSERT INTO af.property_config (order_number,creator_id,is_void,property_id,config_property_id,is_layout_variable) VALUES (2,'1',false,199,147,false);
INSERT INTO af.property_config (order_number,creator_id,is_void,property_id,config_property_id,is_layout_variable) VALUES (3,'1',false,199,151,false);
INSERT INTO af.property_config (order_number,creator_id,is_void,property_id,config_property_id,is_layout_variable) VALUES (4,'1',false,199,156,false);
INSERT INTO af.property_config (order_number,creator_id,is_void,property_id,config_property_id,is_layout_variable) VALUES (5,'1',false,199,157,false);
INSERT INTO af.property_config (order_number,creator_id,is_void,property_id,config_property_id,is_layout_variable) VALUES (6,'1',false,199,158,false);
INSERT INTO af.property_config (order_number,creator_id,is_void,property_id,config_property_id,is_layout_variable) VALUES (7,'1',false,199,192,false);
INSERT INTO af.property_config (order_number,creator_id,is_void,property_id,config_property_id,is_layout_variable) VALUES (8,'1',false,199,19,false);
INSERT INTO af.property_config (order_number,creator_id,is_void,property_id,config_property_id,is_layout_variable) VALUES (9,'1',false,199,20,false);
INSERT INTO af.property_config (order_number,creator_id,is_void,property_id,config_property_id,is_layout_variable) VALUES (10,'1',false,199,160,false);
INSERT INTO af.property_config (order_number,creator_id,is_void,property_id,config_property_id,is_layout_variable) VALUES (11,'1',false,199,161,false);
INSERT INTO af.property_config (order_number,creator_id,is_void,property_id,config_property_id,is_layout_variable) VALUES (12,'1',false,199,162,false);
INSERT INTO af.property_config (order_number,creator_id,is_void,property_id,config_property_id,is_layout_variable) VALUES (13,'1',false,199,163,false);
INSERT INTO af.property_config (order_number,creator_id,is_void,property_id,config_property_id,is_layout_variable) VALUES (14,'1',false,199,164,false);
INSERT INTO af.property_config (order_number,creator_id,is_void,property_id,config_property_id,is_layout_variable) VALUES (15,'1',false,199,165,false);
INSERT INTO af.property_config (order_number,creator_id,is_void,property_id,config_property_id,is_layout_variable) VALUES (16,'1',false,199,166,false);
INSERT INTO af.property_config (order_number,creator_id,is_void,property_id,config_property_id,is_layout_variable) VALUES (17,'1',false,199,167,false);


select setval('af.property_config_id_seq',max(id)) from af.property_config;
select setval('af.property_id_seq',max(id)) from af.property;


--Revert Changes
--rollback DELETE FROM af.property_config WHERE property_id = 199;
--rollback DELETE FROM af.property_config WHERE property_id = 198;
--rollback DELETE FROM af.property_config WHERE id in (352,353);
--rollback DELETE FROM af.property_meta WHERE property_id = 198;
--rollback DELETE FROM af.property_meta WHERE property_id = 199;
--rollback DELETE FROM af.property WHERE id IN (198, 199);
--rollback select setval('af.property_config_id_seq',max(id)) from af.property_config;
--rollback select setval('af.property_id_seq',max(id)) from af.property;