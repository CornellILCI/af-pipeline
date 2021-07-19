--liquibase formatted sql

--changeset postgres:update_labes_design_models context:template splitStatements:false rollbackSplitStatements:false
--comment: BA-325 Update labels of the two new design models


UPDATE af.property
SET "label"='Partially Replicated'
WHERE id=168;

UPDATE af.property
SET "label"='Augmented Design with diagonal checks'
WHERE id=173;


--Revert changes
--rollback UPDATE af.property SET "label"='randPREPirri' WHERE id=168;
--rollback UPDATE af.property SET "label"='randPREPirri' WHERE id=173;
