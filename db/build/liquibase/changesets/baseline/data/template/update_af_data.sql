--liquibase formatted sql

--changeset postgres:update_af_data context:template splitStatements:false rollbackSplitStatements:false
--comment: update_af_data



/*models*/
update af.property set code='randALPHALATTICEcimmyt', name='Alpha-Lattice', is_void=false, tenant_id=2 where id = 118;
update af.property set code='randALPHALATTICEcimmytWHEAT', name='Alpha-Lattice', is_void=false, tenant_id=2 where id = 119;
update af.property set code='randRCBDcimmyt', name='RCBD', is_void=false, tenant_id=2 where id = 120;
update af.property set code='randRCBDirri', name='RCBD', is_void=false, tenant_id=1 where id = 8;
update af.property set code='randALPHALATTICEirri', name='Alpha-Lattice', is_void=false, tenant_id=1 where id = 9;
update af.property SET is_void=true WHERE id IN(38,39);
/*model params*/
UPDATE af.property SET "name"='OCCURRENCES',"label"='No. of Occurrences' WHERE id=65;
UPDATE af.property SET code='entryList',data_type='csv',description='CSV file with the entries information',"name"='ENTRY_LIST',"label"='Entry List' WHERE id=66;
UPDATE af.property SET "name"='REPLICATION_BLOCK' WHERE id=67;
UPDATE af.property SET description='Define field rows and field columns along with the design',"name"='genLayout',"label"='Define Field Shape/dimensions' WHERE id=68;
UPDATE af.property SET "name"='NO_OF_ROWS_PER_REPLICATE' WHERE id=70;
UPDATE af.property SET "name"='REPLICATION_BLOCK' WHERE id=110;
UPDATE af.property SET "name"='BLOCK_SIZE' WHERE id=121;
UPDATE af.property SET description='Number of plots up to the barrier, if Vserpentine=TRUE it is in vertical direction' WHERE id=122;

UPDATE af.property_ui SET minimum=NULL,maximum=NULL WHERE id=47;
UPDATE af.property_ui SET minimum=NULL,maximum=NULL WHERE id=57;
UPDATE af.property_ui SET "default"='false'	WHERE id=60;
UPDATE af.property_config SET is_required=false WHERE id=148;
UPDATE af.property_config SET is_required=false WHERE id=149;
UPDATE af.property_ui SET is_visible=true,"default"='true' WHERE id=63;

UPDATE af.property_ui SET minimum=NULL WHERE id=68;
UPDATE af.property_ui SET is_visible=true WHERE id=72;

UPDATE af.property_config SET is_required=true WHERE id=70;
UPDATE af.property_ui SET maximum=NULL,minimum=NULL WHERE id=17;
UPDATE af.property_ui SET is_disabled=false,"default"=NULL WHERE id=21;
UPDATE af.property_ui SET "default"=NULL WHERE id=23;

UPDATE af.property_config SET is_required=true WHERE id=61;
UPDATE af.property_ui SET minimum=NULL WHERE id=8;
UPDATE af.property_config SET is_required=true WHERE id=62;

/*old meta*/
delete  from af.property_config pc where config_property_id in(30,32,34,35);
delete  from af.property p where id in(30,32,34,35);

insert into af.property_meta(property_id,code,value,creation_timestamp,tenant_id) values
(118,'Rversion','3.4.4',now(),2),
(118,'date','15-Jun-2020',now(),2),
(118,'author','Pedro Barbosa | Alaine Gulles | Rose Imee Zhella Morantte',now(),2),
(118,'email','p.medeiros@cgiar.org',now(),2),
(118,'syntax','Rscript randALPHALATTICEcimmyt.R -e ALPHA_cimmyt_SD_0001.lst --nRep 2 --sBlk 4 --nTrial 2 --genLayout T --nFieldRow 6 --nPlotBarrier 4 --Vserpentine F',now(),2),
(118,'engine','R 3.4.4',now(),2),
(118,'modelVersion','2',now(),2),
(118,'organization_code','CIMMYT',now(),2),
(118,'note','Inherent design restrictions apply',now(),2);

insert into af.property_meta(property_id,code,value,creation_timestamp,tenant_id) values
(119,'Rversion','3.4.4',now(),2),
(119,'date','15-Jun-2020',now(),2),
(119,'author','Pedro Barbosa | Alaine Gulles | Rose Imee Zhella Morantte',now(),2),
(119,'email','p.medeiros@cgiar.org',now(),2),
(119,'syntax','Rscript randALPHALATTICEcimmytWHEAT.R -e ALPHA_cimmyt_wheat_SD_0001.lst --nRep 2 --sBlk 4 --nTrial 2 --genLayout T --nFieldRow 6 --nPlotBarrier 4 --rand1 F --RandOcc T --Vserpentine F',now(),2),
(119,'engine','R 3.4.4',now(),2),
(119,'modelVersion','2',now(),2),
(119,'organization_code','CIMMYT',now(),2),
(119,'note','Inherent design restrictions apply',now(),2);

insert into af.property_meta(property_id,code,value,creation_timestamp,tenant_id) values
(120,'Rversion','3.4.4',now(),2),
(120,'date','14-Jun-2020',now(),2),
(120,'author','Pedro Barbosa | Alaine Gulles | Rose Imee Zhella Morantte',now(),2),
(120,'email','p.medeiros@cgiar.org',now(),2),
(120,'syntax','Rscript randRCBDcimmyt.R -e RCBD_cimmyt_SD_0001.lst --nRep 3 --nTrial 2 --genLayout T --nFieldRow 7 --nPlotBarrier 2 --Vserpentine F',now(),2),
(120,'engine','R 3.4.4',now(),2),
(120,'modelVersion','2',now(),2),
(120,'organization_code','CIMMYT',now(),2);

insert into af.property_meta(property_id,code,value,creation_timestamp,tenant_id) values
(9,'Rversion','3.5.1',now(),1),
(9,'date','22-06-2020',now(),1),
(9,'author','Alaine Gulles | Rose Imee Zhella Morantte',now(),1),
(9,'email','a.gulles@irri.org',now(),1),
(9,'syntax1','Rscript randALPHALATTICEirri.R --entryList "ALPHALATTICE_SD_0001.lst" --nTrial 3 --nRep 4 --nBlk 4 --genLayout F -o ''Output1'' -p ''D:/Results''',now(),1),
(9,'syntax2','Rscript randALPHALATTICEirri.R --entryList "ALPHALATTICE_SD_0001.lst" --nTrial 3 --nRep 4 --nBlk 4 --genLayout T --nRowPerBlk 2 --nRowPerRep 4 --nFieldRow 8 --serpentine F -o ''Output2'' -p ''D:/Results''',now(),1), 
(9,'syntax3','Rscript randALPHALATTICEirri.R --entryList "ALPHALATTICE_SD_0001.lst" --nTrial 3 --nRep 4 --nBlk 4 --genLayout T --nRowPerBlk 2 --nRowPerRep 4 --nFieldRow 8 --serpentine T -o ''Output3'' -p ''D:/Results''',now(),1),
(9,'engine','R 3.4.4',now(),1),
(9,'modelVersion','2',now(),1),
(9,'organization_code','IRRI',now(),1),
(9,'note','Total number of plots per Location Rep should not exceed 1,500.',now(),1);

insert into af.property_meta(property_id,code,value,creation_timestamp,tenant_id) values
(8,'Rversion','3.5.1',now(),1),
(8,'date','22-06-2020',now(),1),
(8,'author','Alaine Gulles | Rose Imee Zhella Morantte',now(),1),
(8,'email','a.gulles@irri.org',now(),1),
(8,'syntax','Rscript randRCBDirri.R --entryList ''RCBD_SD_0001.lst'' --nTrial 3 --nRep 4 --genLayout T --nRowPerRep 5 --nFieldRow 5 --serpentine T -o ''Output'' -p ''D:/Results''',now(),1),
(8,'engine','R 3.4.4',now(),1),
(8,'modelVersion','2',now(),1),
(8,'organization_code','IRRI',now(),1);