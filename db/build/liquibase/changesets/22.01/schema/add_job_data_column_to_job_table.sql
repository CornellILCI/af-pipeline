--liquibase formatted sql

--changeset postgres:add_job_data_column_to_job_table context:schema splitStatements:false rollbackSplitStatements:false
--comment: BA-876 add job_data column to job table.


ALTER TABLE af.job ADD COLUMN job_data jsonb NULL;	-- Job data for the analysis job.

CREATE INDEX "IX_job_data" ON af.job USING gin(job_data);

COMMENT ON COLUMN af.job.job_data IS 'Data used for running the analysis job';

--Revert Changes
--rollback ALTER TABLE af.job DROP COLUMN job_data;
