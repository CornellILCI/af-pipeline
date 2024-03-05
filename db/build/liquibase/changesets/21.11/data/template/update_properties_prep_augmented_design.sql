--liquibase formatted sql

--changeset postgres:update_properties_prep_augmented_design context:template splitStatements:false rollbackSplitStatements:false
--comment: DB-821 Update af.properties p-rep and augmented design



update af.property set name = 'Partially Replicated', label='P-REP' where id = 168;
update af.property set name = 'Augmented Design' where id = 173;


--Revert Changes
--rollback update af.property set name = 'randPREPirri', label='Partially Replicated' where id = 168;
--rollback update af.property set name = 'randAugUnrep' where id = 173;