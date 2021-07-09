--liquibase formatted sql

--changeset postgres:add_request_uuid_reference_in_task_table context:schema splitStatements:false rollbackSplitStatements:false
--comment: DB-282 Create_task_table


ALTER TABLE af.task DROP CONSTRAINT "FK_task_request_uuid";
DROP INDEX af."IXFK_task_request_02";
ALTER TABLE af.task DROP COLUMN request_uuid;
ALTER TABLE af.request DROP CONSTRAINT uuid_unique;

--Revert changes
--rollback ALTER TABLE af.request ADD CONSTRAINT uuid_unique UNIQUE (uuid);
--rollback ALTER TABLE af.task ADD COLUMN request_uuid varchar(50) NULL;
--rollback CREATE INDEX "IXFK_task_request_02" ON af.task (request_uuid ASC);
--rollback ALTER TABLE af.task ADD CONSTRAINT "FK_task_request_uuid" FOREIGN KEY (request_uuid) REFERENCES af.request (uuid) ON DELETE No Action ON UPDATE No Action;