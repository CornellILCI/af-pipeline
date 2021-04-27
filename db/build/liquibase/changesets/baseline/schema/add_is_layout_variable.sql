--liquibase formatted sql

--changeset postgres:add_is_layout_variable context:schema splitStatements:false rollbackSplitStatements:false
--comment: add_is_layout_variable



ALTER TABLE af.property_config 
 ADD COLUMN is_layout_variable boolean NOT NULL   DEFAULT false;
