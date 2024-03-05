--liquibase formatted sql

--changeset postgres:remove_asreml_specific_columns_in_results_table context:schema splitStatements:false rollbackSplitStatements:false
--comment: BA-578 remove asreml specific fields @prediction and @fitted_values and add additional info columns

ALTER TABLE af.prediction
    DROP COLUMN ci95_upper,
    DROP COLUMN ci95_lower;

ALTER TABLE af.fitted_values
    DROP COLUMN rinv_res,
    DROP COLUMN amostat,
    DROP COLUMN amostat_flag,
    DROP COLUMN covariate_trait_value,
    DROP COLUMN trait_qc,
    DROP COLUMN covariate_trait_qc;
