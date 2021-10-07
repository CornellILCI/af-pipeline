--liquibase formatted sql

--changeset postgres:correct_properties_165_and_20 context:template splitStatements:false rollbackSplitStatements:false
--comment: DB-695 Correct properties #165 and #20



UPDATE af.property
SET data_type='*' WHERE id=165;

UPDATE af.property
SET "name"='GxE' WHERE id=20;



--Revert Changes
--rollback UPDATE af.property SET data_type='!I' WHERE id=165;
--rollback UPDATE af.property SET "name"='Gx' WHERE id=20;