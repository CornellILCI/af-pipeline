--liquibase formatted sql

--changeset postgres:design_models_v2.1 context:template splitStatements:false rollbackSplitStatements:false
--comment: design_models_v2.1



ALTER TABLE af.request_entry ADD entry_number int4 NULL;

/*models*/
update af.property set tenant_id = 2, is_void = false, code = 'randROWCOLUMNirri' where id = 38;
update af.property set tenant_id = 2, is_void = false, code = 'randAUGMENTEDRCBDirri' where id = 39;

/* metadata*/
insert into af.property_meta(property_id,code,value,creation_timestamp,tenant_id) values
(38,'Rversion','3.5.1',now(),2),
(38,'date','23-06-2020',now(),2),
(38,'author','Alaine Gulles | Rose Imee Zhella Morantte',now(),2),
(38,'email','a.gulles@irri.org',now(),2),
(38,'syntax1','Rscript randROWCOLUMNirri.R --entryList "ROWCOLUMN_SD_0001.lst" --nTrial 3 --nRep 4 --nRowBlk 4 --genLayout F -o "Output1" -p ''D:/Results''',now(),2),
(38,'syntax2','Rscript randROWCOLUMNirri.R --entryList "ROWCOLUMN_SD_0001.lst" --nTrial 3 --nRep 4 --nRowBlk 4 --genLayout T --nFieldRow 8 --serpentine F -o "Output2" -p ''D:/Results''',now(),2),
(38,'syntax3','Rscript randROWCOLUMNirri.R --entryList "ROWCOLUMN_SD_0001.lst" --nTrial 3 --nRep 4 --nRowBlk 4 --genLayout T --nFieldRow 8 --serpentine T -o "Output3" -p ''D:/Results''',now(),2),
(38,'engine','R 3.4.4',now(),2),
(38,'modelVersion','2',now(),2),
(38,'organization_code','IRRI',now(),2),
(38,'note','Total number of plots per occurrence should not exceed 1,500.',now(),2);

insert into af.property_meta(property_id,code,value,creation_timestamp,tenant_id) values
(39,'Rversion','3.5.1',now(),2),
(39,'date','25-06-2020',now(),2),
(39,'author','Alaine Gulles | Rose Imee Zhella Morantte',now(),2),
(39,'email','a.gulles@irri.org',now(),2),
(39,'syntax1','Rscript randAUGMENTEDRCBDirri.R --entryList "AUGMENTEDRCBD_SD_0001.lst" --nTrial 3 --nRep 4 --genLayout F -o ''Output1'' -p ''D:/Results''',now(),2),
(39,'syntax2','Rscript randAUGMENTEDRCBDirri.R --entryList "AUGMENTEDRCBD_SD_0001.lst" --nTrial 3 --nRep 4 --genLayout T --nRowPerRep 8 --nFieldRow 16 --serpentine F -o ''Output2'' -p ''D:/Results''',now(),2),
(39,'syntax3','Rscript randAUGMENTEDRCBDirri.R --entryList "AUGMENTEDRCBD_SD_0001.lst" --nTrial 3 --nRep 4 --genLayout T --nRowPerRep 8 --nFieldRow 16 --serpentine T -o ''Output3'' -p ''D:/Results''',now(),2),
(39,'engine','R 3.4.4',now(),2),
(39,'modelVersion','2',now(),2),
(39,'organization_code','IRRI',now(),2);

/* configs */
UPDATE af.property_ui SET maximum=NULL,minimum=NULL,is_disabled=true WHERE id=28;
UPDATE af.property_config SET is_layout_variable=true WHERE id=98;
UPDATE af.property_config SET is_layout_variable=true WHERE id=100;

UPDATE af.property_config SET config_property_id=66	WHERE id=119;
delete from af.property_config pc where id = 120;
delete from af.property_ui pu where id = 38;

UPDATE af.property_ui SET minimum=null WHERE id=37;
UPDATE af.property_ui SET "default"='null',is_disabled=false WHERE id=41;
UPDATE af.property_config SET is_layout_variable=true WHERE id in(114,115,116);