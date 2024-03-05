-- Deploy analyticalframework: to pg

--liquibase formatted sql

--changeset postgres:change lenght in analysis.description context:schema splitStatements:false rollbackSplitStatements:false
--comment: change lenght in analysis.description



ALTER TABLE af.analysis 
ALTER COLUMN description TYPE varchar(100);