--liquibase formatted sql

--changeset postgres:change_nfieldcol_to_simple_input context:template splitStatements:false rollbackSplitStatements:false
--comment: DB-850 Change nFieldCol to simple input



update af.property_ui set is_catalogue = false where id = 90;


--Revert Changes
--rollback update af.property_ui set is_catalogue = true where id = 90;