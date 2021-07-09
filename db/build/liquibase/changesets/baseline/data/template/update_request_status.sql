--liquibase formatted sql

--changeset postgres:update_request_status context:template splitStatements:false rollbackSplitStatements:false
--comment: update_request_status



update af.request set status = 'expired';