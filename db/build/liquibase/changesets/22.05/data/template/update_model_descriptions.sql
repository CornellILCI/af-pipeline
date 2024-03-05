--liquibase formatted sql

--changeset postgres:update_model_descriptions context:template splitStatements:false rollbackSplitStatements:false
--comment: DB-1233 Update model descriptions



UPDATE af.property
SET name='RCBD', "label"='RCBD', description= 'Randomize the experiment as a Complete Block Design'
WHERE code = 'randRCBDirri';

UPDATE af.property
SET name='Alpha-Lattice', "label"='Alpha-Lattice', description= 'Randomize the experiment as an Alpha-Lattice Design'
WHERE code = 'randALPHALATTICEirri';

UPDATE af.property
SET name='Row-Column', "label"='Row-Column', description= 'Randomize the experiment as a Row-Column Design'
WHERE code = 'randROWCOLUMNirri';

UPDATE af.property
SET name='Augmented RCB', "label"='Augmented RCB', description= 'Randomize the experiment as an Augmented Randomized Complete Block Design'
WHERE code = 'randAUGMENTEDRCBDirri';

UPDATE af.property
SET name='Alpha-Lattice', "label"='Alpha-Lattice | CIMMYT', description= 'Randomize the experiment as an Alpha-Lattice Design'
WHERE code = 'randALPHALATTICEcimmyt';

UPDATE af.property
SET name='Alpha-Lattice', "label"='IWIN Design', description= 'Randomize the experiment as an Alpha-Lattice Design for IWIN experiments'
WHERE code = 'randALPHALATTICEcimmytWHEAT';

UPDATE af.property
SET name='RCBD', "label"='RCBD | CIMMYT', description= 'Randomize the experiment as a Complete Block Design'
WHERE code = 'randRCBDcimmyt';

UPDATE af.property
SET name='Partially Replicated', "label"='P-REP', description= 'Randomize the experiment as a Partially Replicated Design'
WHERE code = 'randPREPirri';

UPDATE af.property
SET name='Augmented Design', "label"='P-rep CRD w/ diagonal systematic checks', description= 'Randomize the experiment as a Partially Replicated Design with check entries assigned in a Diagonal pattern in the field'
WHERE code = 'randAugUnrep';

UPDATE af.property
SET name='randIBD_OFT', "label"='Incomplete Block| OFT', description= 'Randomize the experiment as an Incomplete Block Design for On-Farm Trial experiments'
WHERE code = 'randIBD_OFT';

UPDATE af.property
SET name='randRCBDirri_OFT', "label"='RCBD | OFT', description= 'Randomize the experiment as aRandomized Complete Block Design for On-Farm Trial experiments'
WHERE code = 'randRCBDirri_OFT';