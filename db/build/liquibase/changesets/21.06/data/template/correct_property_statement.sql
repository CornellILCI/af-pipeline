--liquibase formatted sql

--changeset postgres:correct_property_statement context:template splitStatements:false rollbackSplitStatements:false
--comment: BA-483 correct property #150 statement



UPDATE af.property
SET "statement"='{trait_name} ~ mu rep !r entry rep.block !f mv'
WHERE id=150;



--Revert Changes
--rollback UPDATE af.property SET "statement"='{trait_name} mu rep !r entry rep.block !f mv' WHERE id=150;
