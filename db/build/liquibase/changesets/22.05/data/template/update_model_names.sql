--liquibase formatted sql

--changeset postgres:update_model_names context:template splitStatements:false rollbackSplitStatements:false
--comment: DB-1239 Update OFT model names



update af.property set name = 'Incomplete Block Design' where code = 'randIBD_OFT';
update af.property set name = 'On-Farm Trial RCBD' where code = 'randRCBDirri_OFT';