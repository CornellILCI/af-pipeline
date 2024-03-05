--liquibase formatted sql

--changeset postgres:update_property_name_label context:schema splitStatements:false rollbackSplitStatements:false
--comment: BA-11 Add analysis configuration data



ALTER TABLE af.property ADD statement varchar(250) NULL;
COMMENT ON COLUMN af.property.statement IS 'A command, instruction, piece of code, etc., associated to the property';

ALTER TABLE af.property ALTER COLUMN "name" TYPE varchar(70) USING "name"::varchar;
ALTER TABLE af.property ALTER COLUMN "label" TYPE varchar(70) USING "label"::varchar;
ALTER TABLE af.property_meta ALTER COLUMN "code" TYPE varchar(30) USING "code"::varchar;