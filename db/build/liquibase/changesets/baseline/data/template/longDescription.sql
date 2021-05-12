--liquibase formatted sql

--changeset postgres:longDescription context:template splitStatements:false rollbackSplitStatements:false
--comment: longDescription



ALTER TABLE af.property ALTER COLUMN description TYPE varchar(150) USING description::varchar;

update af.property set description = 'contains the arrangement of the plot numbers in a location rep, if genLayout is TRUE' where id = 125;
update af.property set description = 'contains the arrangement of the replicates (super-block) in a location rep , if genLayout is TRUE' where id = 126;
update af.property set description = 'contains the arrangement of the treatments (entries) per location rep, if genLayout is TRUE' where id = 127;
update af.property set description = 'Whether plots will be assing in Vertical serpentine arrangement or Horizontal' where id = 123;
update af.property set description = 'Field ordering for the generation of rows and columns' where id = 71;
update af.property set description = 'Prefix to be used for the names of the output files' where id = 72;
update af.property set description = 'contains information on the parameters used to generate the randomization' where id = 97;
update af.property set description = 'contains the arrangement of the plot numbers in a location rep, if genLayout is TRUE' where id = 99;
update af.property set description = 'contains the arrangement of the replicates in a location rep , if genLayout is TRUE' where id = 100;
update af.property set description = 'spreadsheet file showing the result of  the randomization (and layout, if generated)' where id = 96;