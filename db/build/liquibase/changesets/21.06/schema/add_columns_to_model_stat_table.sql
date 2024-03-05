--liquibase formatted sql

--changeset postgres:add_columns_to_model_stat_table context:schema splitStatements:false rollbackSplitStatements:false
--comment: BA-484 add columns to model_stat table



ALTER TABLE af.model_stat 
 ADD COLUMN conclusion varchar(500) NULL;	-- Last message the engine generates after running the job.

ALTER TABLE af.model_stat 
 ADD COLUMN is_converged boolean NULL;	-- Whether the model has converged or not.

COMMENT ON COLUMN af.model_stat.conclusion
	IS 'Last message the engine generates after running the job.'
;

COMMENT ON COLUMN af.model_stat.is_converged
	IS 'Whether the model has converged or not.'
;


--Revert Changes
--rollback ALTER TABLE af.model_stat DROP COLUMN conclusion;
--rollback ALTER TABLE af.model_stat DROP COLUMN is_converged;

