--liquibase formatted sql

--changeset postgres:add_columns_to save_request_data_to_analysis_table context:schema splitStatements:false rollbackSplitStatements:false
--comment: BA-749 Add columns to save request data to analysis table.



ALTER TABLE af.analysis 
 ADD COLUMN formula_id integer NULL;	-- Reference to the formula stored in the property table.

ALTER TABLE af.analysis 
 ADD COLUMN residual_id integer NULL;	-- Reference to the residual id stored in the property table.

ALTER TABLE af.analysis 
 ADD COLUMN trait_analysis_pattern_id integer NULL;	-- Reference to the trait analysis pattern id stored in the property table.

ALTER TABLE af.analysis 
 ADD COLUMN exp_loc_pattern_id integer NULL;	-- Reference to the experiment location pattern id stored in the property table.

ALTER TABLE af.analysis 
 ADD COLUMN analysis_objective_id integer NULL;	-- Reference to the analysis objective id stored in the property table.

ALTER TABLE af.analysis 
 ADD COLUMN analysis_request_data jsonb NULL;	-- Relevant data of the analysis request

ALTER TABLE af.analysis 
 ADD COLUMN additional_info jsonb NULL;	-- Additional info related to the analysis


CREATE INDEX "IX_additional_info" ON af.analysis USING gin(additional_info)
;

CREATE INDEX "IX_analays_request_data" ON af.analysis USING gin(analysis_request_data)
;

ALTER TABLE af.analysis ADD CONSTRAINT "FK_analysis_property_analysis"
	FOREIGN KEY (analysis_objective_id) REFERENCES  af.property(id) ON DELETE No Action ON UPDATE No Action
;

ALTER TABLE af.analysis ADD CONSTRAINT "FK_analysis_property_formula"
	FOREIGN KEY (formula_id) REFERENCES  af.property(id) ON DELETE No Action ON UPDATE No Action
;

ALTER TABLE af.analysis ADD CONSTRAINT "FK_analysis_property_residual"
	FOREIGN KEY (residual_id) REFERENCES  af.property(id) ON DELETE No Action ON UPDATE No Action
;

ALTER TABLE af.analysis ADD CONSTRAINT "FK_analysis_property_trait"
	FOREIGN KEY (trait_analysis_pattern_id) REFERENCES  af.property(id) ON DELETE No Action ON UPDATE No Action
;

ALTER TABLE af.analysis ADD CONSTRAINT "FK_analysis_property_exp"
	FOREIGN KEY (exp_loc_pattern_id) REFERENCES  af.property(id) ON DELETE No Action ON UPDATE No Action
;

COMMENT ON COLUMN af.analysis.additional_info
	IS 'Additional info related to the analysis'
;

COMMENT ON COLUMN af.analysis.analysis_objective_id
	IS 'Reference to the analysis objective id stored in the property table.'
;

COMMENT ON COLUMN af.analysis.analysis_request_data
	IS 'Relevant data of the analysis request'
;

COMMENT ON COLUMN af.analysis.exp_loc_pattern_id
	IS 'Reference to the experiment location pattern id stored in the property table.'
;

COMMENT ON COLUMN af.analysis.formula_id
	IS 'Reference to the formula stored in the property table.'
;

COMMENT ON COLUMN af.analysis.residual_id
	IS 'Reference to the residual id stored in the property table.'
;

COMMENT ON COLUMN af.analysis.trait_analysis_pattern_id
	IS 'Reference to the trait analysis pattern id stored in the property table.'
;


--Revert Changes
--rollback ALTER TABLE af.analysis DROP COLUMN formula_id;
--rollback ALTER TABLE af.analysis DROP COLUMN residual_id;
--rollback ALTER TABLE af.analysis DROP COLUMN trait_analysis_pattern_id;
--rollback ALTER TABLE af.analysis DROP COLUMN exp_loc_pattern_id;
--rollback ALTER TABLE af.analysis DROP COLUMN analysis_objective_id;
--rollback ALTER TABLE af.analysis DROP COLUMN analysis_request_data;
--rollback ALTER TABLE af.analysis DROP COLUMN additional_info;