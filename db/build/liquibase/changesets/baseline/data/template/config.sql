--liquibase formatted sql

--changeset postgres:config context:template splitStatements:false rollbackSplitStatements:false
--comment: config



--
-- Dropping constraints from af.property_config
--
ALTER TABLE af.property_config
  DROP CONSTRAINT "FK_property_config_property";
ALTER TABLE af.property_config
  DROP CONSTRAINT "FK_property_config_property_ui";

--
-- Dropping constraints from af.property_rule
--
ALTER TABLE af.property_rule
  DROP CONSTRAINT "FK_property_rule_property";
ALTER TABLE af.property_rule
  DROP CONSTRAINT "FK_property_rule_property_config";

--
-- Dropping constraints from af.request
--
ALTER TABLE af.request
  DROP CONSTRAINT "FK_request_property";

--
-- Dropping constraints from af.request_parameter
--
ALTER TABLE af.request_parameter
  DROP CONSTRAINT "FK_request_parameter_property";
ALTER TABLE af.request_parameter
  DROP CONSTRAINT "FK_request_parameter_request";

--
-- Inserting data into table af.property
--
INSERT INTO af.property(id, code, name, creation_timestamp, modification_timestamp, creator_id, modifier_id, is_void, label, description, type, data_type) VALUES
(1, 'objective', 'Objective', null, null, null, null, false, 'Objective', 'Objective', 'catalog_root', 'character varying'),
(2, 'trait_pattern', 'Trait Pattern', null, null, null, null, false, 'Trait Analysis Pattern', 'Trait Analysis Pattern', 'catalog_root', 'character varying'),
(3, 'exptloc_analysis_pattern', 'Exp Loc Analysis Pattern', null, null, null, null, false, 'Experiment/Location Analysis Pattern', 'Experiment/Location Analysis Pattern', 'catalog_root', 'character varying'),
(4, 'model', 'Design Model', null, null, null, null, false, 'Model', 'Model configuration', 'catalog_root', 'character varying'),
(5, 'prediction', 'Prediction', null, null, null, null, false, 'Prediction', 'Prediction', 'catalog_root', 'character varying'),
(6, 'error', 'Error', null, null, null, null, false, 'Error', 'Error', 'catalog_root', 'character varying'),
(7, 'obj_pred', 'Prediction', null, null, null, null, false, null, null, 'catalog_item', 'integer'),
(8, 'runRCBD', 'Randomized Complete Block', null, null, null, null, false, null, null, 'catalog_item', 'integer'),
(9, 'runALPHALATTIC', 'Alpha Lattice', null, null, null, null, false, null, null, 'catalog_item', 'integer'),
(10, 'uv', 'Univariate', null, null, null, null, false, null, null, 'catalog_item', 'integer'),
(11, 'bv', 'Bivariate', null, null, null, null, false, null, null, 'catalog_item', 'integer'),
(12, 'cv', 'Covariate', null, null, null, null, false, null, null, 'catalog_item', 'integer'),
(13, 'mt', 'Multi trait', null, null, null, null, false, null, null, 'catalog_item', 'integer'),
(14, 'se', 'Series', null, null, null, null, false, null, null, 'catalog_item', 'integer'),
(15, 'SESL', 'Single Experiment - Single Location', null, null, null, null, false, null, null, 'catalog_item', 'integer'),
(16, 'SEML', 'Single Experiment - Multiple Location', null, null, null, null, false, null, null, 'catalog_item', 'integer'),
(17, 'MESL', 'Multiple Experiment - Single Location', null, null, null, null, false, null, null, 'catalog_item', 'integer'),
(18, 'MEML', 'Multiple Experiment - Multiple Location', null, null, null, null, false, null, null, 'catalog_item', 'integer'),
(19, 'g', 'G', null, null, null, null, false, null, null, 'catalog_item', 'integer'),
(20, 'gxe', 'Gx', null, null, null, null, false, null, null, 'catalog_item', 'integer'),
(21, 'gxt', 'GxT', null, null, null, null, false, null, null, 'catalog_item', 'integer'),
(22, 'gxm', 'GxM', null, null, null, null, false, null, null, 'catalog_item', 'integer'),
(23, 'AR1XAR1_2_0', 'AR1XAR1_2_0', null, null, null, null, false, null, null, 'catalog_item', 'integer'),
(24, 'AR1XAR1_0_0', 'AR1XAR1_0_0', null, null, null, null, false, null, null, 'catalog_item', 'integer'),
(25, 'NO_AR1XAR1_ID', 'NO_AR1XAR1_ID', null, null, null, null, false, null, null, 'catalog_item', 'integer'),
(26, 'NO_AR1XAR1', 'NO_AR1XAR1', null, null, null, null, false, null, null, 'catalog_item', 'integer'),
(30, 'engine', 'ASReml', null, null, null, null, false, null, null, 'meta', 'character varying'),
(32, 'version', 'v.4', null, null, null, null, false, null, null, 'meta', 'character varying'),
(34, 'path', '/nala/analysis/models/SARCBD.as', null, null, null, null, false, null, null, 'meta', 'character varying'),
(35, 'config_trait_level', 'plot', null, null, null, null, false, null, null, 'meta', 'character varying'),
(38, 'runROWCOLUMN', 'Row-Column', '2020-04-27 13:38:21.6540000', null, null, null, false, null, null, 'catalog_item', 'integer'),
(39, 'runAUGMENTEDRCBD', 'Augmented RCB', '2020-04-27 13:38:21.6540000', null, null, null, false, null, null, 'catalog_item', 'integer'),
(65, 'nTrial', 'OCCURRANCES', null, null, null, null, false, 'No. of Occurrances', 'Number of occurrances within the experiment', 'input', 'integer'),
(66, 'nTreatment', 'ENTRY_COUNT_CONT', null, null, null, null, false, 'No. of Entries', 'Total number of entries', 'input', 'integer'),
(67, 'nRep', 'REP_COUNT', null, null, null, null, false, 'No. of Replicates', 'Number of replicates', 'input', 'integer'),
(68, 'genLayout', 'DEFINE_SHAP', null, null, null, null, false, 'Define Shape/Dimension', 'Define rows and columns along with the design', 'input', 'boolean'),
(69, 'nFieldRow', 'ROW', null, null, null, null, false, 'Rows', 'Total number of rows', 'input', 'integer'),
(70, 'nRowPerRep', 'NO_OF_ROWS_PER_BLOCK', null, null, null, null, false, 'No. of rows per rep', 'Number of rows per replicate', 'input', 'integer'),
(71, 'serpentine', 'FLD_ORDER', null, null, null, null, false, 'Field Order', 'Field ordering for the generation of rows and colu', 'input', 'boolean'),
(72, 'outputFile', 'OUTPUT_FIL', null, null, null, null, false, 'Output File', 'Prefix to be used for the names of the output file', 'input', 'character varying'),
(73, 'outputPath', 'OUTPUT_PATH', null, null, null, null, false, 'Output Path', 'Path where output will be saved', 'input', 'character varying'),
(96, 'fieldbook', 'fieldbook', null, null, null, null, false, 'Randomization Fieldbook file', 'spreadsheet file showing the result of  the random', 'output', 'csv'),
(97, 'designInfo', 'designInfo', null, null, null, null, false, 'Design information file', 'contains information on the parameters used to gen', 'output', 'txt'),
(98, 'StatisticalDesignArray', 'StatisticalDesignArray', null, null, null, null, false, 'Statistical design array file', 'contains the arrangement of the treatments in the ', 'output', 'csv'),
(99, 'PlotNumLayout', 'PlotNumLayout', null, null, null, null, false, 'Plot number arrangement file (Layout)', 'contains the arrangement of the plot numbers in a ', 'output', 'csv'),
(100, 'RepLayout', 'RepLayout', null, null, null, null, false, 'Replication arrangement file', 'contains the arrangement of the replicates in a lo', 'output', 'csv'),
(101, 'TrmtLayout', 'TrmtLayout', null, null, null, null, false, 'Treatment arrangement file', 'contains the arrangement of the treatments per loc', 'output', 'csv'),
(110, 'nBlk', 'TREATMENT_BLOCK', null, null, null, null, false, 'No. of Blocks per Rep', 'Number of blocks per rep', 'input', 'integer'),
(111, 'nRowPerBlk', 'NO_OF_ROWS_PER_BLOCK', null, null, null, null, false, 'No. of rows per block', 'Number of rows per block', 'input', 'integer'),
(112, 'nRowBlk', 'ROW_BLOCK', null, null, null, null, false, 'No. of Row Blocks', 'Number of row blocks', 'input', 'integer'),
(113, 'nCheckTreatment', 'ENTRY_COUNT_CONT', null, null, null, null, false, 'No. of Check Entries', 'Number of Check entries', 'input', 'integer'),
(114, 'nTestTreatment', 'ENTRY_COUNT_CONT', null, null, null, null, false, 'No. of Test Entries', 'Number of test entries', 'input', 'integer'),
(115, 'BlockLayout', 'BlockLayout', null, null, null, null, false, 'Block arrangement file (Layout)', 'contains the arrangement of the blocks within repl', 'output', 'csv'),
(116, 'RowBlockLayout', 'RowBlockLayout', null, null, null, null, false, 'Row Block arrangement file (Layout)', 'contains the arrangement of the row blocks within ', 'output', 'csv'),
(117, 'ColumnBlockLayout', 'ColumnBlockLayout', null, null, null, null, false, 'Column Block arrangement file (Layout)', 'contains the arrangement of the column blocks with', 'output', 'csv'),
(118, 'ALPHALATTICE_cimmyt', 'Alpha-Lattice(cimmyt)', null, null, null, null, null, null, null, 'catalog_item', 'integer'),
(119, 'ALPHALATTICE_wheat', 'Alpha-Lattice (wheat)', null, null, null, null, null, null, null, 'catalog_item', 'integer'),
(120, 'RCBD', 'Randomized Complete Block(cimmyt)', null, null, null, null, null, null, null, 'catalog_item', 'integer'),
(121, 'sBlk', 'TREATMENT_BLOCK', null, null, null, null, false, 'No. of plots per block', 'Block size, it is the number of plots in each bloc', 'input', 'integer'),
(122, 'nPlotBarrier', 'ROW', null, null, null, null, false, 'Plots until turn the serpentine', 'Number of plots up to the barrier, if Vserpentine=', 'input', 'integer'),
(123, 'Vserpentine', 'FLD_ORDER', null, null, null, null, false, 'Field Order', 'Whether plots will be assing in Vertical serpentin', 'input', 'boolean'),
(124, 'LayoutBlock', 'LayoutBlock', null, null, null, null, false, 'Block arrangement file (Layout)', 'contains the arrangement of the blocks within repl', 'output', 'csv'),
(125, 'LayoutPlots', 'LayoutPlots', null, null, null, null, false, 'Plot number arrangement file (Layout)', 'contains the arrangement of the plot numbers in a ', 'output', 'csv'),
(126, 'LayoutRep', 'LayoutRep', null, null, null, null, false, 'Replication arrangement file', 'contains the arrangement of the replicates (super-', 'output', 'csv'),
(127, 'LayoutEntry', 'LayoutEntry', null, null, null, null, false, 'Treatment arrangement file', 'contains the arrangement of the treatments (entrie', 'output', 'csv'),
(128, 'rand1', 'FLD_ORDER', null, null, null, null, false, 'Randomize the 1st rep', 'Whether the first rep should be randomized', 'input', 'boolean'),
(130, 'experimentId', 'EXPT_ID', null, null, null, null, false, 'Experiment Id', null, 'request_meta', 'integer');

--
-- Inserting data into table af.property_config
--
INSERT INTO af.property_config(id, property_id, config_property_id, property_ui_id, creation_timestamp, modification_timestamp, creator_id, modifier_id, is_void, is_required, order_number) VALUES
(1, 1, 1, 1, '2020-05-06 10:01:32.6596490', null, '1', null, false, true, 1),
(2, 2, 2, 2, '2020-05-06 10:01:32.6596490', null, '1', null, false, true, 1),
(3, 3, 3, 3, '2020-05-06 10:01:32.6596490', null, '1', null, false, true, 1),
(4, 4, 4, 4, '2020-05-06 10:01:32.6596490', null, '1', null, false, true, 1),
(5, 5, 5, 5, '2020-05-06 10:01:32.6596490', null, '1', null, false, true, 1),
(6, 6, 6, 6, '2020-05-06 10:01:32.6596490', null, '1', null, false, true, 1),
(7, 1, 7, 1, '2020-05-06 10:24:28.7105090', null, '1', null, false, false, 1),
(8, 2, 10, null, '2020-05-06 10:24:28.7105090', null, '1', null, false, false, 1),
(9, 2, 11, null, '2020-05-06 10:24:28.7105090', null, '1', null, false, false, 2),
(10, 2, 12, null, '2020-05-06 10:24:28.7105090', null, '1', null, false, false, 3),
(11, 2, 13, null, '2020-05-06 10:24:28.7105090', null, '1', null, false, false, 4),
(12, 2, 14, null, '2020-05-06 10:24:28.7105090', null, '1', null, false, false, 5),
(13, 3, 15, null, '2020-05-06 10:24:28.7105090', null, '1', null, false, false, 1),
(14, 3, 16, null, '2020-05-06 10:24:28.7105090', null, '1', null, false, false, 2),
(15, 3, 17, null, '2020-05-06 10:24:28.7105090', null, '1', null, false, false, 3),
(16, 3, 18, null, '2020-05-06 10:24:28.7105090', null, '1', null, false, false, 4),
(17, 4, 8, null, '2020-05-06 10:24:28.7105090', null, '1', null, false, false, 1),
(18, 4, 9, null, '2020-05-06 10:24:28.7105090', null, '1', null, false, false, 2),
(19, 4, 38, null, '2020-05-06 10:24:28.7105090', null, '1', null, false, false, 3),
(20, 4, 39, null, '2020-05-06 10:24:28.7105090', null, '1', null, false, false, 4),
(21, 5, 19, null, '2020-05-06 10:24:28.7105090', null, '1', null, false, false, 1),
(22, 5, 20, null, '2020-05-06 10:24:28.7105090', null, '1', null, false, false, 2),
(23, 5, 21, null, '2020-05-06 10:24:28.7105090', null, '1', null, false, false, 3),
(24, 5, 22, null, '2020-05-06 10:24:28.7105090', null, '1', null, false, false, 4),
(25, 6, 23, null, '2020-05-06 10:24:28.7105090', null, '1', null, false, false, 1),
(26, 6, 24, null, '2020-05-06 10:24:28.7105090', null, '1', null, false, false, 2),
(27, 6, 25, null, '2020-05-06 10:24:28.7105090', null, '1', null, false, false, 3),
(28, 6, 26, null, '2020-05-06 10:24:28.7105090', null, '1', null, false, false, 4),
(29, 8, 30, null, '2020-05-06 10:24:28.7105090', null, '1', null, false, false, 1),
(30, 8, 32, null, '2020-05-06 10:24:28.7105090', null, '1', null, false, false, 2),
(31, 8, 34, null, '2020-05-06 10:24:28.7105090', null, '1', null, false, false, 3),
(32, 8, 35, null, '2020-05-06 10:24:28.7105090', null, '1', null, false, false, 4),
(61, 8, 65, 7, '2020-05-05 18:01:26.5985930', null, '1', null, false, true, 1),
(62, 8, 66, 8, '2020-05-05 18:01:26.5985930', null, '1', null, false, true, 2),
(63, 8, 67, 9, '2020-05-05 18:01:26.5985930', null, '1', null, false, true, 3),
(64, 8, 68, 10, '2020-05-05 18:01:26.5985930', null, '1', null, false, true, 4),
(65, 8, 69, 11, '2020-05-05 18:01:26.5985930', null, '1', null, false, true, 5),
(66, 8, 70, 12, '2020-05-05 18:01:26.5985930', null, '1', null, false, true, 6),
(67, 8, 71, 13, '2020-05-05 18:01:26.5985930', null, '1', null, false, true, 7),
(68, 8, 72, 14, '2020-05-05 18:01:26.5985930', null, '1', null, false, true, 8),
(69, 8, 73, 15, '2020-05-05 18:01:26.5985930', null, '1', null, false, true, 9),
(70, 9, 65, 16, '2020-05-05 18:01:26', null, '1', null, false, false, 1),
(71, 8, 96, null, '2020-05-05 18:01:26.5985930', null, '1', null, false, true, 1),
(72, 8, 97, null, '2020-05-05 18:01:26.5985930', null, '1', null, false, true, 2),
(73, 8, 98, null, '2020-05-05 18:01:26.5985930', null, '1', null, false, true, 3),
(74, 8, 99, null, '2020-05-05 18:01:26.5985930', null, '1', null, false, true, 4),
(75, 8, 100, null, '2020-05-05 18:01:26.5985930', null, '1', null, false, true, 5),
(76, 8, 101, null, '2020-05-05 18:01:26.5985930', null, '1', null, false, true, 6),
(77, 9, 66, 17, '2020-05-05 18:01:26.5985930', null, '1', null, false, true, 2),
(78, 9, 67, 18, '2020-05-05 18:01:26.5985930', null, '1', null, false, true, 3),
(79, 9, 68, 20, '2020-05-05 18:01:26.5985930', null, '1', null, false, true, 5),
(80, 9, 69, 23, '2020-05-05 18:01:26.5985930', null, '1', null, false, false, 8),
(81, 9, 70, 22, '2020-05-05 18:01:26.5985930', null, '1', null, false, true, 7),
(82, 9, 71, 24, '2020-05-05 18:01:26.5985930', null, '1', null, false, true, 9),
(83, 9, 72, 25, '2020-05-05 18:01:26.5985930', null, '1', null, false, true, 10),
(84, 9, 73, 26, '2020-05-05 18:01:26.5985930', null, '1', null, false, true, 11),
(85, 9, 110, 19, '2020-05-05 18:01:26.5985930', null, '1', null, false, true, 4),
(86, 9, 111, 21, '2020-05-05 18:01:26.5985930', null, '1', null, false, true, 6),
(87, 9, 96, null, '2020-05-05 18:01:26.5985930', null, '1', null, false, true, 1),
(88, 9, 97, null, '2020-05-05 18:01:26.5985930', null, '1', null, false, true, 2),
(89, 9, 98, null, '2020-05-05 18:01:26.5985930', null, '1', null, false, true, 3),
(90, 9, 115, null, '2020-05-05 18:01:26.5985930', null, '1', null, false, true, 4),
(91, 9, 99, null, '2020-05-05 18:01:26.5985930', null, '1', null, false, true, 5),
(92, 9, 100, null, '2020-05-05 18:01:26.5985930', null, '1', null, false, true, 6),
(93, 9, 101, null, '2020-05-05 18:01:26.5985930', null, '1', null, false, true, 7),
(94, 38, 65, 27, '2020-05-05 18:01:26.5985930', null, '1', null, false, true, 1),
(95, 38, 66, 28, '2020-05-05 18:01:26.5985930', null, '1', null, false, true, 2),
(96, 38, 67, 29, '2020-05-05 18:01:26.5985930', null, '1', null, false, true, 3),
(97, 38, 68, 31, '2020-05-05 18:01:26.5985930', null, '1', null, false, true, 5),
(98, 38, 69, 32, '2020-05-05 18:01:26.5985930', null, '1', null, false, false, 6),
(99, 38, 112, 30, '2020-05-05 18:01:26.5985930', null, '1', null, false, true, 4),
(100, 38, 71, 33, '2020-05-05 18:01:26.5985930', null, '1', null, false, true, 7),
(101, 38, 72, 34, '2020-05-05 18:01:26.5985930', null, '1', null, false, true, 8),
(102, 38, 73, 35, '2020-05-05 18:01:26.5985930', null, '1', null, false, true, 9),
(103, 38, 96, null, '2020-05-05 18:01:26.5985930', null, '1', null, false, true, 1),
(104, 38, 97, null, '2020-05-05 18:01:26.5985930', null, '1', null, false, true, 2),
(105, 38, 98, null, '2020-05-05 18:01:26.5985930', null, '1', null, false, true, 3),
(106, 38, 99, null, '2020-05-05 18:01:26.5985930', null, '1', null, false, true, 4),
(107, 38, 100, null, '2020-05-05 18:01:26.5985930', null, '1', null, false, true, 5),
(108, 38, 101, null, '2020-05-05 18:01:26.5985930', null, '1', null, false, true, 6),
(109, 38, 116, null, '2020-05-05 18:01:26.5985930', null, '1', null, false, true, 7),
(110, 38, 117, null, '2020-05-05 18:01:26.5985930', null, '1', null, false, true, 8),
(111, 39, 65, 36, '2020-05-05 18:01:26.5985930', null, '1', null, false, true, 1),
(112, 39, 67, 39, '2020-05-05 18:01:26.5985930', null, '1', null, false, true, 4),
(113, 39, 68, 40, '2020-05-05 18:01:26.5985930', null, '1', null, false, true, 5),
(114, 39, 69, 41, '2020-05-05 18:01:26.5985930', null, '1', null, false, true, 6),
(115, 39, 70, 42, '2020-05-05 18:01:26.5985930', null, '1', null, false, true, 7),
(116, 39, 71, 43, '2020-05-05 18:01:26.5985930', null, '1', null, false, true, 8),
(117, 39, 72, 44, '2020-05-05 18:01:26.5985930', null, '1', null, false, true, 9),
(118, 39, 73, 45, '2020-05-05 18:01:26.5985930', null, '1', null, false, true, 10),
(119, 39, 113, 37, '2020-05-05 18:01:26.5985930', null, '1', null, false, true, 2),
(120, 39, 114, 38, '2020-05-05 18:01:26.5985930', null, '1', null, false, true, 3),
(121, 39, 96, null, '2020-05-05 18:01:26.5985930', null, '1', null, false, true, 1),
(122, 39, 97, null, '2020-05-05 18:01:26.5985930', null, '1', null, false, true, 2),
(123, 39, 98, null, '2020-05-05 18:01:26.5985930', null, '1', null, false, true, 3),
(124, 39, 99, null, '2020-05-05 18:01:26.5985930', null, '1', null, false, true, 4),
(125, 39, 100, null, '2020-05-05 18:01:26.5985930', null, '1', null, false, true, 5),
(126, 39, 101, null, '2020-05-05 18:01:26.5985930', null, '1', null, false, true, 6),
(127, 118, 65, 46, '2020-05-08 04:18:20.4635360', null, '1', null, false, true, 1),
(128, 118, 66, 47, '2020-05-08 04:18:20.5279630', null, '1', null, false, true, 2),
(129, 118, 67, 48, '2020-05-08 04:18:20.5914520', null, '1', null, false, true, 3),
(130, 118, 121, 49, '2020-05-08 04:18:20.6549850', null, '1', null, false, true, 4),
(131, 118, 68, 50, '2020-05-08 04:18:20.7120840', null, '1', null, false, true, 5),
(132, 118, 69, 51, '2020-05-08 04:18:20.7692030', null, '1', null, false, false, 6),
(133, 118, 122, 52, '2020-05-08 04:18:20.8285010', null, '1', null, false, false, 7),
(134, 118, 123, 53, '2020-05-08 04:18:20.8796620', null, '1', null, false, true, 8),
(135, 118, 72, 54, '2020-05-08 04:18:20.9307590', null, '1', null, false, true, 9),
(136, 118, 73, 55, '2020-05-08 04:18:20.9825460', null, '1', null, false, true, 10),
(137, 118, 96, null, '2020-05-08 04:18:21.0326830', null, '1', null, false, true, 1),
(138, 118, 97, null, '2020-05-08 04:18:21.0889550', null, '1', null, false, true, 2),
(139, 118, 124, null, '2020-05-08 04:18:21.1475400', null, '1', null, false, true, 3),
(140, 118, 125, null, '2020-05-08 04:18:21.2221660', null, '1', null, false, true, 4),
(141, 118, 126, null, '2020-05-08 04:18:21.2789810', null, '1', null, false, true, 5),
(142, 118, 127, null, '2020-05-08 04:18:21.3557670', null, '1', null, false, true, 6),
(143, 119, 65, 56, '2020-05-08 04:26:19.6236020', null, '1', null, false, true, 1),
(144, 119, 66, 57, '2020-05-08 04:26:19.6880130', null, '1', null, false, true, 2),
(145, 119, 67, 58, '2020-05-08 04:26:19.7466040', null, '1', null, false, true, 3),
(146, 119, 121, 59, '2020-05-08 04:26:19.8019660', null, '1', null, false, true, 4),
(147, 119, 68, 60, '2020-05-08 04:26:19.8716260', null, '1', null, false, true, 5),
(148, 119, 69, 61, '2020-05-08 04:26:19.9339830', null, '1', null, false, true, 6),
(149, 119, 122, 62, '2020-05-08 04:26:19.9871320', null, '1', null, false, true, 7),
(150, 119, 128, 63, '2020-05-08 04:26:20.0440850', null, '1', null, false, true, 8),
(151, 119, 123, 64, '2020-05-08 04:26:20.0964820', null, '1', null, false, true, 9),
(152, 119, 72, 65, '2020-05-08 04:26:20.1538080', null, '1', null, false, true, 10),
(153, 119, 73, 66, '2020-05-08 04:26:20.2049260', null, '1', null, false, true, 11),
(154, 119, 96, null, '2020-05-08 04:26:20.2580330', null, '1', null, false, true, 1),
(155, 119, 97, null, '2020-05-08 04:26:20.3206290', null, '1', null, false, true, 2),
(156, 119, 124, null, '2020-05-08 04:26:20.3761540', null, '1', null, false, true, 3),
(157, 119, 125, null, '2020-05-08 04:26:20.4332590', null, '1', null, false, true, 4),
(158, 119, 126, null, '2020-05-08 04:26:20.4849330', null, '1', null, false, true, 5),
(159, 119, 127, null, '2020-05-08 04:26:20.5429400', null, '1', null, false, true, 6),
(160, 120, 65, 67, '2020-05-08 04:36:24.2259500', null, '1', null, false, true, 1),
(161, 120, 66, 68, '2020-05-08 04:36:24.2889330', null, '1', null, false, true, 2),
(162, 120, 67, 69, '2020-05-08 04:36:24.3397610', null, '1', null, false, true, 3),
(163, 120, 68, 70, '2020-05-08 04:36:24.4032050', null, '1', null, false, true, 4),
(164, 120, 69, 71, '2020-05-08 04:36:24.4630110', null, '1', null, false, true, 5),
(165, 120, 122, 72, '2020-05-08 04:36:24.5175170', null, '1', null, false, true, 6),
(166, 120, 123, 73, '2020-05-08 04:36:24.5683100', null, '1', null, false, true, 7),
(167, 120, 128, 74, '2020-05-08 04:36:24.6278290', null, '1', null, false, true, 8),
(168, 120, 72, 75, '2020-05-08 04:36:24.6825470', null, '1', null, false, true, 9),
(169, 120, 73, 76, '2020-05-08 04:36:24.7433790', null, '1', null, false, true, 10),
(170, 120, 96, null, '2020-05-08 04:36:24.8144280', null, '1', null, false, true, 1),
(171, 120, 97, null, '2020-05-08 04:36:24.8729880', null, '1', null, false, true, 2),
(172, 120, 125, null, '2020-05-08 04:36:24.9299980', null, '1', null, false, true, 3),
(173, 120, 124, null, '2020-05-08 04:36:24.9872160', null, '1', null, false, true, 4),
(174, 120, 127, null, '2020-05-08 04:36:25.0380360', null, '1', null, false, true, 5),
(175, 4, 118, null, '2020-05-08 11:54:52.7633610', null, '1', null, false, false, 5),
(176, 4, 119, null, '2020-05-08 11:54:52.8405870', null, '1', null, false, false, 6),
(177, 4, 120, null, '2020-05-08 11:54:52.8962900', null, '1', null, false, false, 7);

--
-- Inserting data into table af.property_rule
--
INSERT INTO af.property_rule(id, property_config_id, property_id, creation_timestamp, modification_timestamp, creator_id, modifier_id, is_void, type, expression, "group") VALUES
(2, 77, 66, null, null, null, null, false, 'allowed-value', 'not-prime', 1),
(3, 128, 66, null, null, null, null, false, 'allowed-value', 'not-prime', 1),
(4, 144, 66, null, null, null, null, false, 'allowed-value', 'not-prime', 1),
(5, 65, 68, null, null, null, null, false, 'required-if', 'is-true', 1),
(6, 80, 68, null, null, null, null, false, 'required-if', 'is-true', 1),
(7, 98, 68, null, null, null, null, false, 'required-if', 'is-true', 1),
(8, 114, 68, null, null, null, null, false, 'required-if', 'is-true', 1),
(9, 132, 68, null, null, null, null, false, 'required-if', 'is-true', 1),
(10, 148, 68, null, null, null, null, false, 'required-if', 'is-true', 1),
(11, 164, 68, null, null, null, null, false, 'required-if', 'is-true', 1),
(12, 86, 68, null, null, null, null, false, 'required-if', 'is-true', 1),
(13, 82, 68, null, null, null, null, false, 'required-if', 'is-true', 1),
(14, 67, 68, null, null, null, null, false, 'required-if', 'is-true', 1),
(15, 100, 68, null, null, null, null, false, 'required-if', 'is-true', 1),
(16, 116, 68, null, null, null, null, false, 'required-if', 'is-true', 1),
(17, 134, 68, null, null, null, null, false, 'required-if', 'is-true', 1),
(18, 151, 68, null, null, null, null, false, 'required-if', 'is-true', 1),
(19, 166, 68, null, null, null, null, false, 'required-if', 'is-true', 1),
(20, 133, 68, null, null, null, null, false, 'required-if', 'is-true', 1),
(21, 149, 68, null, null, null, null, false, 'required-if', 'is-true', 1),
(22, 165, 68, null, null, null, null, false, 'required-if', 'is-true', 1),
(25, 146, 68, null, null, null, null, false, 'required-if', 'is-true', 1),
(26, 130, 66, null, null, null, null, false, 'allowed-value', 'is-factor-of', 1),
(27, 146, 66, null, null, null, null, false, 'allowed-value', 'is-factor-of', 2),
(28, 150, 68, null, null, null, null, false, 'required-if', 'is-true', 1);

--
-- Inserting data into table af.property_ui
--
INSERT INTO af.property_ui(id, is_visible, minimum, maximum, unit, "default", is_disabled, is_multiple, is_catalogue, creation_timestamp, modification_timestamp, creator_id, modifier_id, is_void) VALUES
(1, true, null, null, null, null, false, false, true, null, null, null, null, null),
(2, true, null, null, null, null, false, false, true, null, null, null, null, null),
(3, true, null, null, null, null, false, false, true, null, null, null, null, null),
(4, true, null, null, null, null, false, false, true, null, null, null, null, null),
(5, true, null, null, null, null, false, true, true, null, null, null, null, null),
(6, true, null, null, null, null, false, false, true, null, null, null, null, null),
(7, true, 1, null, null, null, false, false, false, null, null, null, null, null),
(8, false, 2, null, null, null, true, false, false, null, null, null, null, null),
(9, true, 2, null, null, null, false, false, false, null, null, null, null, null),
(10, false, null, null, null, 'false', false, false, false, null, null, null, null, null),
(11, true, 1, null, null, null, false, false, false, null, null, null, null, null),
(12, true, 1, null, null, null, false, false, false, null, null, null, null, null),
(13, false, null, null, null, 'false', false, false, false, null, null, null, null, null),
(14, false, null, null, null, null, true, false, false, null, null, null, null, null),
(15, false, null, null, null, null, true, false, false, null, null, null, null, null),
(16, true, 1, null, null, null, false, false, false, null, null, null, null, null),
(17, false, 9, 750, null, 'true', true, false, false, null, null, null, null, null),
(18, true, 2, 166, null, null, false, false, false, null, null, null, null, null),
(19, true, 2, 375, null, null, false, false, false, null, null, null, null, null),
(20, false, null, null, null, 'false', false, false, false, null, null, null, null, null),
(21, true, 1, 375, null, 'false', true, false, false, null, null, null, null, null),
(22, true, 1, 750, null, null, false, false, false, null, null, null, null, null),
(23, true, 1, 1500, null, 'false', false, false, false, null, null, null, null, null),
(24, false, null, null, null, 'false', false, false, false, null, null, null, null, null),
(25, false, null, null, null, null, true, false, false, null, null, null, null, null),
(26, false, null, null, null, null, true, false, false, null, null, null, null, null),
(27, true, 1, null, null, null, false, false, false, null, null, null, null, null),
(28, false, 9, 750, null, null, false, false, false, null, null, null, null, null),
(29, true, 2, 166, null, null, false, false, false, null, null, null, null, null),
(30, true, 3, 250, null, null, false, false, false, null, null, null, null, null),
(31, false, null, null, null, 'false', false, false, false, null, null, null, null, null),
(32, true, 3, 500, null, null, false, false, false, null, null, null, null, null),
(33, false, null, null, null, 'false', false, false, false, null, null, null, null, null),
(34, false, null, null, null, null, true, false, false, null, null, null, null, null),
(35, false, null, null, null, null, true, false, false, null, null, null, null, null),
(36, true, 1, null, null, null, false, false, false, null, null, null, null, null),
(37, false, 2, null, null, null, true, false, false, null, null, null, null, null),
(38, false, 2, null, null, null, true, false, false, null, null, null, null, null),
(39, true, 2, null, null, null, false, false, false, null, null, null, null, null),
(40, false, null, null, null, 'false', false, false, false, null, null, null, null, null),
(41, true, 1, null, null, 'false', true, false, false, null, null, null, null, null),
(42, true, 1, null, null, null, false, false, false, null, null, null, null, null),
(43, false, null, null, null, 'false', false, false, false, null, null, null, null, null),
(44, false, null, null, null, null, true, false, false, null, null, null, null, null),
(45, false, null, null, null, null, true, false, false, null, null, null, null, null),
(46, true, 1, null, null, null, false, false, false, null, null, null, null, null),
(47, false, 9, 10000, null, null, true, false, false, null, null, null, null, null),
(48, true, 2, 4, null, null, false, false, false, null, null, null, null, null),
(49, true, 2, 100, null, null, false, false, false, null, null, null, null, null),
(50, false, null, null, null, 'false', false, false, false, null, null, null, null, null),
(51, true, 1, 10000, null, null, false, false, false, null, null, null, null, null),
(52, true, 1, null, null, null, false, false, false, null, null, null, null, null),
(53, false, null, null, null, 'false', false, false, false, null, null, null, null, null),
(54, false, null, null, null, null, true, false, false, null, null, null, null, null),
(55, false, null, null, null, null, true, false, false, null, null, null, null, null),
(56, true, 1, null, null, null, false, false, false, null, null, null, null, null),
(57, false, 9, 10000, null, null, true, false, false, null, null, null, null, null),
(58, true, 2, 4, null, null, false, false, false, null, null, null, null, null),
(59, true, 2, 100, null, null, false, false, false, null, null, null, null, null),
(60, false, null, null, null, null, false, false, false, null, null, null, null, null),
(61, true, 1, 10000, null, null, false, false, false, null, null, null, null, null),
(62, true, 1, null, null, null, false, false, false, null, null, null, null, null),
(63, false, null, null, null, 'false', false, false, false, null, null, null, null, null),
(64, false, null, null, null, 'false', false, false, false, null, null, null, null, null),
(65, false, null, null, null, null, true, false, false, null, null, null, null, null),
(66, false, null, null, null, null, true, false, false, null, null, null, null, null),
(67, true, 1, null, null, null, false, false, false, null, null, null, null, null),
(68, false, 2, null, null, null, true, false, false, null, null, null, null, null),
(69, true, 2, null, null, null, false, false, false, null, null, null, null, null),
(70, false, null, null, null, 'false', false, false, false, null, null, null, null, null),
(71, true, 1, null, null, null, false, false, false, null, null, null, null, null),
(72, false, 1, null, null, null, false, false, false, null, null, null, null, null),
(73, false, null, null, null, 'false', false, false, false, null, null, null, null, null),
(74, false, null, null, null, 'true', false, false, false, null, null, null, null, null),
(75, false, null, null, null, null, true, false, false, null, null, null, null, null),
(76, false, null, null, null, null, true, false, false, null, null, null, null, null);

--
-- Inserting data into table af.request
--
INSERT INTO af.request(id, uuid, category, type, method_id, design, requestor_id, institute, crop, program, status, creation_timestamp, modification_timestamp, creator_id, modifier_id, is_void) VALUES
(1, 'c1444c0d-d698-4ec6-9d18-02d96fb358c3', 1, 'Trial Design', 8, 'runRCBD', 1, 'CIMMYT', 'wheat', 'GWP', 'new', null, null, '0', '0', false),
(2, '74124352-2128-4e91-8cab-db42eccf687c', 1, 'Trial Design', 8, 'runRCBD', 1, 'CIMMYT', 'wheat', 'GWP', 'new', null, null, '0', '0', false),
(3, '49f7270f-59b5-4545-845a-cfed8f8c0ae8', 1, 'Trial Design', 8, 'runRCBD', 1, 'CIMMYT', 'wheat', 'GWP', 'new', null, null, '0', '0', false),
(4, '523505e9-d075-4bc9-ac38-283b44e1799a', 1, 'Trial Design', 8, 'runRCBD', 1, 'CIMMYT', 'wheat', 'GWP', 'new', null, null, '0', '0', false),
(5, '8cab3374-9ed3-4faf-b883-db96ce10c91c', 1, 'Trial Design', 8, 'runRCBD', 1, 'CIMMYT', 'wheat', 'GWP', 'new', '2020-05-11 16:55:04.2340000', null, '1', '0', false),
(6, '30f07335-5e88-4044-8be1-1dd4832feafa', 1, 'Trial Design', 8, 'runRCBD', 1, 'CIMMYT', 'wheat', 'GWP', 'new', '2020-05-12 01:49:33.8510000', null, '1', '0', false),
(7, 'af8f5645-60a3-42a2-a0ef-9d04fc688202', 1, 'Trial Design', 8, 'runRCBD', 1, 'CIMMYT', 'wheat', 'GWP', 'new', '2020-05-12 01:52:03.7370000', null, '1', '0', false),
(8, '105db338-a261-4d2a-aada-073630bcd28b', 1, 'Trial Design', 8, 'runRCBD', 1, 'CIMMYT', 'wheat', 'GWP', 'new', '2020-05-12 01:55:20.6910000', null, '1', '0', false),
(9, '3b87bd73-a4b9-4c7a-b147-767cf9572e44', 1, 'Trial Design', 8, 'runRCBD', 1, 'CIMMYT', 'wheat', 'GWP', 'new', '2020-05-12 01:57:25.5730000', null, '1', '0', false),
(10, '52974e67-07ad-4fa9-83ec-c90d134f3df3', 1, 'Trial Design', 8, 'runRCBD', 1, 'CIMMYT', 'wheat', 'GWP', 'new', '2020-05-12 02:01:38.5320000', null, '1', '0', false),
(11, '2b74ef31-694c-471c-8afd-0d0acea232a5', 1, 'Trial Design', 8, 'runRCBD', 1, 'CIMMYT', 'wheat', 'GWP', 'new', '2020-05-12 02:04:07.6480000', null, '1', '0', false),
(12, '1107658c-5a6c-4453-a560-9c04fd178a7c', 1, 'Trial Design', 8, 'runRCBD', 1, 'CIMMYT', 'wheat', 'GWP', 'new', '2020-05-12 02:05:10.5090000', null, '1', '0', false),
(13, 'b54ee7c9-1ffe-44a4-bf34-d6c6248b1d55', 1, 'Trial Design', 8, 'runRCBD', 1, 'CIMMYT', 'wheat', 'GWP', 'new', '2020-05-12 02:27:39.5020000', null, '1', '0', false),
(14, '10aafdaf-ae6a-4b09-9307-98f2c8d3b7e3', 1, 'Trial Design', 8, 'RCD', 1, 'CIMMYT', 'wheat', 'GWP', 'new', '2020-05-12 02:29:34.5630000', null, '1', '0', false),
(15, 'f7882655-129c-4a33-acae-90adf7f1af9d', 1, 'Trial Design', 8, 'RCB', 1, 'CIMMYT', 'wheat', 'GWP', 'new', '2020-05-12 15:18:21.0840000', null, '1', '0', false);

--
-- Inserting data into table af.request_parameter
--
INSERT INTO af.request_parameter(id, property_id, value, creation_timestamp, modification_timestamp, creator_id, modifier_id, is_void, request_id) VALUES
(1, 130, '123', null, null, '0', '0', false, 2),
(2, 130, '123', null, null, '0', '0', false, 3),
(3, 130, '123', null, null, '0', '0', false, 4),
(4, 130, '123', '2020-05-11 16:55:04.3200000', null, '1', '0', false, 5),
(5, 130, '123', '2020-05-12 01:49:33.9590000', null, '1', '0', false, 6),
(6, 130, '123', '2020-05-12 01:52:03.8300000', null, '1', '0', false, 7),
(7, 130, '123', '2020-05-12 01:55:20.9390000', null, '1', '0', false, 8),
(8, 130, '123', '2020-05-12 01:57:25.6800000', null, '1', '0', false, 9),
(9, 130, '123', '2020-05-12 02:01:38.6280000', null, '1', '0', false, 10),
(10, 65, '100', '2020-05-12 02:04:07.7640000', null, '1', '0', false, 11),
(11, 66, '3', '2020-05-12 02:04:07.8270000', null, '1', '0', false, 11),
(12, 67, 'true', '2020-05-12 02:04:07.8820000', null, '1', '0', false, 11),
(13, 72, '/myFolder', '2020-05-12 02:04:07.9360000', null, '1', '0', false, 11),
(14, 73, 'myReq.json', '2020-05-12 02:04:07.9940000', null, '1', '0', false, 11),
(15, 68, '3', '2020-05-12 02:04:08.0480000', null, '1', '0', false, 11),
(16, 69, '2', '2020-05-12 02:04:08.1730000', null, '1', '0', false, 11),
(17, 70, '1', '2020-05-12 02:04:08.2820000', null, '1', '0', false, 11),
(18, 71, 'true', '2020-05-12 02:04:08.3880000', null, '1', '0', false, 11),
(19, 130, '123', '2020-05-12 02:04:08.5030000', null, '1', '0', false, 11),
(20, 65, '100', '2020-05-12 02:05:10.5660000', null, '1', '0', false, 12),
(21, 66, '3', '2020-05-12 02:05:10.6710000', null, '1', '0', false, 12),
(22, 67, 'true', '2020-05-12 02:05:10.7740000', null, '1', '0', false, 12),
(23, 73, '/myFolder', '2020-05-12 02:05:10.8780000', null, '1', '0', false, 12),
(24, 72, 'myReq.json', '2020-05-12 02:05:10.9870000', null, '1', '0', false, 12),
(25, 68, '3', '2020-05-12 02:05:11.0920000', null, '1', '0', false, 12),
(26, 69, '2', '2020-05-12 02:05:11.1970000', null, '1', '0', false, 12),
(27, 70, '1', '2020-05-12 02:05:11.2970000', null, '1', '0', false, 12),
(28, 71, 'true', '2020-05-12 02:05:11.3970000', null, '1', '0', false, 12),
(29, 130, '123', '2020-05-12 02:05:11.4970000', null, '1', '0', false, 12),
(30, 65, '100', '2020-05-12 02:27:39.6130000', null, '1', '0', false, 13),
(31, 66, '3', '2020-05-12 02:27:39.6760000', null, '1', '0', false, 13),
(32, 67, 'true', '2020-05-12 02:27:39.7300000', null, '1', '0', false, 13),
(33, 73, '/myFolder', '2020-05-12 02:27:39.7840000', null, '1', '0', false, 13),
(34, 72, 'myReq.json', '2020-05-12 02:27:39.8390000', null, '1', '0', false, 13),
(35, 68, '3', '2020-05-12 02:27:39.8980000', null, '1', '0', false, 13),
(36, 69, '2', '2020-05-12 02:27:40.0030000', null, '1', '0', false, 13),
(37, 70, '1', '2020-05-12 02:27:40.1100000', null, '1', '0', false, 13),
(38, 71, 'true', '2020-05-12 02:27:40.2210000', null, '1', '0', false, 13),
(39, 130, '123', '2020-05-12 02:27:40.3350000', null, '1', '0', false, 13),
(40, 65, '100', '2020-05-12 02:29:34.6240000', null, '1', '0', false, 14),
(41, 66, '3', '2020-05-12 02:29:34.7280000', null, '1', '0', false, 14),
(42, 67, 'true', '2020-05-12 02:29:34.8520000', null, '1', '0', false, 14),
(43, 73, '/myFolder', '2020-05-12 02:29:35.0060000', null, '1', '0', false, 14),
(44, 72, 'myReq.json', '2020-05-12 02:29:35.1100000', null, '1', '0', false, 14),
(45, 68, '3', '2020-05-12 02:29:35.2380000', null, '1', '0', false, 14),
(46, 69, '2', '2020-05-12 02:29:35.3410000', null, '1', '0', false, 14),
(47, 70, '1', '2020-05-12 02:29:35.4560000', null, '1', '0', false, 14),
(48, 71, 'true', '2020-05-12 02:29:35.5650000', null, '1', '0', false, 14),
(49, 130, '123', '2020-05-12 02:29:35.6710000', null, '1', '0', false, 14),
(50, 65, '100', '2020-05-12 15:18:21.1400000', null, '1', '0', false, 15),
(51, 66, '3', '2020-05-12 15:18:21.1460000', null, '1', '0', false, 15),
(52, 67, 'true', '2020-05-12 15:18:21.1500000', null, '1', '0', false, 15),
(53, 73, '/myFolder', '2020-05-12 15:18:21.1530000', null, '1', '0', false, 15),
(54, 72, 'myReq.json', '2020-05-12 15:18:21.1560000', null, '1', '0', false, 15),
(55, 68, '3', '2020-05-12 15:18:21.1610000', null, '1', '0', false, 15),
(56, 69, '2', '2020-05-12 15:18:21.1640000', null, '1', '0', false, 15),
(57, 70, '1', '2020-05-12 15:18:21.1670000', null, '1', '0', false, 15),
(58, 71, 'true', '2020-05-12 15:18:21.1700000', null, '1', '0', false, 15),
(59, 130, '123', '2020-05-12 15:18:21.1730000', null, '1', '0', false, 15);

--
-- Creating constraints for af.property_config
--
ALTER TABLE af.property_config
   ADD FOREIGN KEY (property_id) REFERENCES af.property(id);
ALTER TABLE af.property_config
   ADD FOREIGN KEY (property_ui_id) REFERENCES af.property_ui(id);

--
-- Creating constraints for af.property_rule
--
ALTER TABLE af.property_rule
   ADD FOREIGN KEY (property_id) REFERENCES af.property(id);
ALTER TABLE af.property_rule
   ADD FOREIGN KEY (property_config_id) REFERENCES af.property_config(id);

--
-- Creating constraints for af.request
--
ALTER TABLE af.request
   ADD FOREIGN KEY (method_id) REFERENCES af.property(id);

--
-- Creating constraints for af.request_parameter
--
ALTER TABLE af.request_parameter
   ADD FOREIGN KEY (property_id) REFERENCES af.property(id);
ALTER TABLE af.request_parameter
   ADD FOREIGN KEY (request_id) REFERENCES af.request(id);
